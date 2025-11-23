"""
Main ETL orchestration script.
"""
import asyncio
import os
import sys
from datetime import datetime
from typing import Optional
import argparse

# Add src to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from utils.logger import setup_logger, setup_file_logger
from extractors import IDRDExtractor, CSVExtractor, APIExtractor
from transformers import DataCleaner, DataValidator, DataNormalizer
from loaders import DatabaseLoader


class ETLPipeline:
    """Main ETL pipeline orchestrator."""
    
    def __init__(self, source: str, config: dict = None):
        """
        Initialize ETL pipeline.
        
        Args:
            source: Data source (idrd, csv, api)
            config: Configuration dict
        """
        self.source = source
        self.config = config or {}
        self.logger = setup_logger("etl")
        self.file_logger, self.log_file_path = setup_file_logger("etl")
        
        # Get database URL from environment
        self.database_url = os.getenv(
            'DATABASE_URL',
            'postgresql+asyncpg://triqueta_user:triqueta_pass@db:5432/triqueta_db'
        )
        
        # Statistics
        self.stats = {
            'extracted': 0,
            'cleaned': 0,
            'valid': 0,
            'invalid': 0,
            'normalized': 0,
            'loaded': 0,
            'failed': 0,
            'errors': []
        }
    
    async def run(self) -> dict:
        """
        Run the complete ETL pipeline.
        
        Returns:
            Dict with execution statistics
        """
        try:
            self.logger.info(f"Starting ETL pipeline for source: {self.source}")
            start_time = datetime.now()
            
            # 1. Extract
            records = await self._extract()
            self.stats['extracted'] = len(records)
            
            if not records:
                self.logger.warning("No records extracted. Exiting.")
                return self.stats
            
            # 2. Transform - Clean
            cleaner = DataCleaner(self.logger)
            records = await cleaner.clean(records)
            self.stats['cleaned'] = len(records)
            
            # 3. Transform - Validate
            validator = DataValidator(self.logger)
            valid_records, invalid_records = await validator.validate(records)
            self.stats['valid'] = len(valid_records)
            self.stats['invalid'] = len(invalid_records)
            
            if not valid_records:
                self.logger.error("No valid records after validation. Exiting.")
                return self.stats
            
            # 4. Transform - Normalize
            normalizer = DataNormalizer(self.logger)
            normalized_records = await normalizer.normalize(valid_records)
            self.stats['normalized'] = len(normalized_records)
            
            # 5. Load
            loader = DatabaseLoader(self.database_url, self.logger)
            loaded, failed, errors = await loader.load(normalized_records)
            self.stats['loaded'] = loaded
            self.stats['failed'] = failed
            self.stats['errors'] = errors
            
            await loader.close()
            
            # Final statistics
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.logger.info("=" * 60)
            self.logger.info("ETL Pipeline Complete!")
            self.logger.info(f"Duration: {duration:.2f} seconds")
            self.logger.info(f"Extracted: {self.stats['extracted']}")
            self.logger.info(f"Cleaned: {self.stats['cleaned']}")
            self.logger.info(f"Valid: {self.stats['valid']}")
            self.logger.info(f"Invalid: {self.stats['invalid']}")
            self.logger.info(f"Normalized: {self.stats['normalized']}")
            self.logger.info(f"Loaded: {self.stats['loaded']}")
            self.logger.info(f"Failed: {self.stats['failed']}")
            self.logger.info(f"Log file: {self.log_file_path}")
            self.logger.info("=" * 60)
            
            return self.stats
            
        except Exception as e:
            self.logger.error(f"ETL pipeline failed: {e}", exc_info=True)
            self.stats['errors'].append(str(e))
            raise
    
    async def _extract(self):
        """Extract data from configured source."""
        self.logger.info(f"Extracting from source: {self.source}")
        
        if self.source == 'idrd':
            extractor = IDRDExtractor(self.logger)
            return await extractor.extract(self.config)
            
        elif self.source == 'csv':
            extractor = CSVExtractor(self.logger)
            return await extractor.extract(self.config)
            
        elif self.source == 'api':
            extractor = APIExtractor(self.logger)
            return await extractor.extract(self.config)
            
        else:
            raise ValueError(f"Unknown source: {self.source}")


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Triqueta Digital ETL')
    parser.add_argument(
        '--source',
        type=str,
        default='idrd',
        choices=['idrd', 'csv', 'api'],
        help='Data source to extract from'
    )
    parser.add_argument(
        '--csv-path',
        type=str,
        help='Path to CSV file (required if source=csv)'
    )
    parser.add_argument(
        '--api-url',
        type=str,
        help='API URL (required if source=api)'
    )
    
    args = parser.parse_args()
    
    # Build config
    config = {}
    if args.source == 'csv':
        if not args.csv_path:
            parser.error("--csv-path is required when source=csv")
        config['file_path'] = args.csv_path
    elif args.source == 'api':
        if not args.api_url:
            parser.error("--api-url is required when source=api")
        config['url'] = args.api_url
    
    # Run pipeline
    pipeline = ETLPipeline(source=args.source, config=config)
    await pipeline.run()


if __name__ == '__main__':
    asyncio.run(main())
