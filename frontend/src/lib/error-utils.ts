/**
 * Utility functions for error handling
 */

/**
 * Extracts a user-friendly error message from various error types.
 * Handles Axios errors, FastAPI validation errors, network errors, and generic errors.
 * 
 * @param error - The error object (can be Error, AxiosError, or unknown)
 * @returns A user-friendly error message string
 */
export function getErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    // Axios error with response
    if ('response' in error && error.response) {
      const axiosError = error as any;
      const detail = axiosError.response?.data?.detail;
      
      if (typeof detail === 'string') {
        return detail;
      }
      
      if (Array.isArray(detail)) {
        // FastAPI validation errors come as an array of objects
        return detail.map((d: any) => d.msg || d.message || JSON.stringify(d)).join(', ');
      }
      
      if (typeof detail === 'object' && detail !== null) {
        return detail.msg || detail.message || JSON.stringify(detail);
      }
    }
    
    // Network error or other Error
    return error.message || 'Ocurrió un error inesperado';
  }
  
  return 'Ocurrió un error inesperado';
}

