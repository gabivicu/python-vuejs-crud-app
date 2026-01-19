/**
 * Loading state composable.
 * Demonstrates reusable loading state management.
 */
import { ref } from 'vue'

export function useLoading(initialState = false) {
  const loading = ref(initialState)
  const loadingMessage = ref('')

  function startLoading(message = '') {
    loading.value = true
    loadingMessage.value = message
  }

  function stopLoading() {
    loading.value = false
    loadingMessage.value = ''
  }

  async function withLoading(asyncFn, message = '') {
    try {
      startLoading(message)
      return await asyncFn()
    } finally {
      stopLoading()
    }
  }

  return {
    loading,
    loadingMessage,
    startLoading,
    stopLoading,
    withLoading,
  }
}
