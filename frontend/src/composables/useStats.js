import { itemService } from '../api'

export function useStats() {
  const stats = {
    total: 0,
    completed: 0,
    pending: 0,
    overdue: 0,
    completion_rate: 0,
    priority_stats: {},
    category_stats: {}
  }

  const loading = { value: false }
  const error = { value: null }

  /**
   * Fetches statistics from API
   * @returns {Promise<void>}
   */
  const fetchStats = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await itemService.getStats()
      Object.assign(stats, response.data)
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch statistics'
      console.error('Error fetching stats:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    stats,
    loading,
    error,
    fetchStats
  }
}
