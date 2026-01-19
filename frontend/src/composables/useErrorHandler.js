/**
 * Error handling composable.
 * Demonstrates centralized error handling patterns.
 */
import { ref } from 'vue'

export function useErrorHandler() {
  const error = ref(null)
  const isError = ref(false)

  function handleError(err) {
    isError.value = true
    if (err.response) {
      // Server responded with error
      error.value = err.response.data?.detail || 
                    err.response.data?.message || 
                    `Server error: ${err.response.status}`
    } else if (err.request) {
      // Request made but no response
      error.value = 'Network error. Please check your connection.'
    } else {
      // Something else happened
      error.value = err.message || 'An unexpected error occurred'
    }
    console.error('Error:', err)
  }

  function clearError() {
    error.value = null
    isError.value = false
  }

  return {
    error,
    isError,
    handleError,
    clearError,
  }
}
