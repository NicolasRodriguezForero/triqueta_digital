"""
Seed data script for Triqueta Digital MVP.
Creates initial data for testing and demo purposes.
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import Usuario, Actividad, ActividadEstado
from app.core.security import get_password_hash
import os
from datetime import datetime, timedelta


async def seed_database():
    """Seed database with initial data."""
    
    # Database URL
    database_url = os.getenv(
        'DATABASE_URL',
        'postgresql+asyncpg://triqueta_user:triqueta_pass@localhost:5432/triqueta_db'
    )
    
    print(f"🌱 Seeding database: {database_url}")
    
    engine = create_async_engine(database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # 1. Create admin user
        print("Creating admin user...")
        admin = Usuario(
            email="admin@triqueta.digital",
            nombre_completo="Admin Triqueta",
            hashed_password=get_password_hash("admin123"),
            is_admin=True,
            fecha_registro=datetime.utcnow()
        )
        session.add(admin)
        
        # 2. Create regular users
        print("Creating regular users...")
        users = [
            Usuario(
                email="maria@example.com",
                nombre_completo="María González",
                hashed_password=get_password_hash("password123"),
                is_admin=False,
                fecha_registro=datetime.utcnow()
            ),
            Usuario(
                email="carlos@example.com",
                nombre_completo="Carlos Rodríguez",
                hashed_password=get_password_hash("password123"),
                is_admin=False,
                fecha_registro=datetime.utcnow()
            ),
            Usuario(
                email="ana@example.com",
                nombre_completo="Ana Martínez",
                hashed_password=get_password_hash("password123"),
                is_admin=False,
                fecha_registro=datetime.utcnow()
            ),
        ]
        
        for user in users:
            session.add(user)
        
        # 3. Create sample activities
        print("Creating sample activities...")
        activities = [
            Actividad(
                nombre="Ciclovía Chapinero",
                descripcion="Espacio recreativo para ciclistas todos los domingos en Chapinero",
                tipo="Deporte",
                localidad="Chapinero",
                direccion="Carrera 7 desde Calle 72 hasta Calle 100",
                fecha_inicio=datetime.now().date(),
                fecha_fin=(datetime.now() + timedelta(days=365)).date(),
                horario="Domingos 7:00 AM - 2:00 PM",
                precio=0.0,
                es_gratuita=True,
                contacto_telefono="60112345678",
                contacto_email="ciclovia@bogota.gov.co",
                etiquetas=["ciclismo", "deporte", "recreación", "familias"],
                fuente="Manual",
                estado=ActividadEstado.APROBADA
            ),
            Actividad(
                nombre="Cine al Parque",
                descripcion="Proyección gratuita de cine colombiano en parques de la ciudad",
                tipo="Cultura",
                localidad="Chapinero",
                direccion="Parque El Virrey",
                fecha_inicio=(datetime.now() + timedelta(days=7)).date(),
                fecha_fin=(datetime.now() + timedelta(days=7)).date(),
                horario="19:00 - 21:00",
                precio=0.0,
                es_gratuita=True,
                contacto_telefono="60112345679",
                contacto_email="cultura@bogota.gov.co",
                etiquetas=["cine", "cultura", "entretenimiento"],
                fuente="Manual",
                estado=ActividadEstado.APROBADA
            ),
            Actividad(
                nombre="Yoga en el Parque",
                descripcion="Clases gratuitas de yoga para todos los niveles",
                tipo="Recreación",
                localidad="Santa Fe",
                direccion="Parque de los Periodistas",
                fecha_inicio=datetime.now().date(),
                fecha_fin=(datetime.now() + timedelta(days=90)).date(),
                horario="Sábados y domingos 8:00 AM - 10:00 AM",
                precio=0.0,
                es_gratuita=True,
                contacto_telefono="60112345680",
                contacto_email="recreacion@bogota.gov.co",
                etiquetas=["yoga", "bienestar", "salud"],
                fuente="Manual",
                estado=ActividadEstado.APROBADA
            ),
            Actividad(
                nombre="Concierto Sinfónica",
                descripcion="Concierto de la Orquesta Filarmónica de Bogotá",
                tipo="Cultura",
                localidad="La Candelaria",
                direccion="Teatro Colón - Calle 10",
                fecha_inicio=(datetime.now() + timedelta(days=14)).date(),
                fecha_fin=(datetime.now() + timedelta(days=14)).date(),
                horario="20:00 - 22:00",
                precio=30000.0,
                es_gratuita=False,
                contacto_telefono="60112345681",
                contacto_email="teatro@bogota.gov.co",
                contacto_web="https://teatrocolon.gov.co",
                etiquetas=["música", "clásica", "orquesta"],
                fuente="Manual",
                estado=ActividadEstado.APROBADA
            ),
            Actividad(
                nombre="Taller de Pintura Comunitario",
                descripcion="Taller gratuito de pintura para todas las edades",
                tipo="Cultura",
                localidad="Santa Fe",
                direccion="Casa de la Cultura Santa Fe",
                fecha_inicio=(datetime.now() + timedelta(days=5)).date(),
                fecha_fin=(datetime.now() + timedelta(days=60)).date(),
                horario="Martes y jueves 10:00 AM - 12:00 PM",
                precio=0.0,
                es_gratuita=True,
                contacto_telefono="60112345682",
                contacto_email="cultura@santafe.gov.co",
                etiquetas=["arte", "pintura", "taller"],
                fuente="Manual",
                estado=ActividadEstado.APROBADA
            ),
        ]
        
        for activity in activities:
            session.add(activity)
        
        # Commit all changes
        await session.commit()
        
        print("✅ Database seeded successfully!")
        print(f"   - Created 1 admin user (admin@triqueta.digital / admin123)")
        print(f"   - Created {len(users)} regular users")
        print(f"   - Created {len(activities)} sample activities")
    
    await engine.dispose()


if __name__ == '__main__':
    print("🌱 Starting seed process...")
    asyncio.run(seed_database())
