/**
 * Pinia store for items management.
 * Demonstrates centralized state management and separation of concerns.
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { itemService } from '../api'

export const useItemsStore = defineStore('items', () => {
  // State
  const items = ref([])
  const loading = ref(false)
  const error = ref(null)
  const filters = ref({
    category: '',
    priority: '',
    completed: '',
    due_filter: '',
    search: '',
  })
  const sortBy = ref('-created_at')
  const selectedItems = ref([])
  const stats = ref({
    total: 0,
    completed: 0,
    pending: 0,
    overdue: 0,
    completion_rate: 0,
    priority_stats: {},
    category_stats: {},
  })

  // Getters (computed)
  const completedItems = computed(() =>
    items.value.filter(item => item.completed)
  )

  const pendingItems = computed(() =>
    items.value.filter(item => !item.completed)
  )

  const overdueItems = computed(() =>
    items.value.filter(item => {
      if (!item.due_date || item.completed) return false
      return new Date(item.due_date) < new Date()
    })
  )

  const filteredItems = computed(() => {
    let filtered = [...items.value]

    if (filters.value.category) {
      filtered = filtered.filter(item => item.category === filters.value.category)
    }
    if (filters.value.priority) {
      filtered = filtered.filter(item => item.priority === filters.value.priority)
    }
    if (filters.value.completed !== '') {
      const completed = filters.value.completed === 'true'
      filtered = filtered.filter(item => item.completed === completed)
    }
    if (filters.value.search) {
      const searchLower = filters.value.search.toLowerCase()
      filtered = filtered.filter(item =>
        item.title.toLowerCase().includes(searchLower) ||
        item.description.toLowerCase().includes(searchLower) ||
        (item.tags && item.tags.toLowerCase().includes(searchLower))
      )
    }

    return filtered
  })

  const hasActiveFilters = computed(() => {
    return Object.values(filters.value).some(value => value !== '')
  })

  // Actions
  async function fetchItems() {
    loading.value = true
    error.value = null
    try {
      const params = {
        ordering: sortBy.value,
        ...Object.fromEntries(
          Object.entries(filters.value).filter(([_, v]) => v !== '')
        ),
      }
      const response = await itemService.getAll(params)
      items.value = response.data.results || response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch items'
      console.error('Error fetching items:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchStats() {
    try {
      const response = await itemService.getStats()
      stats.value = response.data
    } catch (err) {
      console.error('Error fetching stats:', err)
    }
  }

  async function createItem(data) {
    loading.value = true
    error.value = null
    try {
      const response = await itemService.create(data)
      items.value.unshift(response.data)
      await fetchStats()
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to create item'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateItem(id, data) {
    loading.value = true
    error.value = null
    try {
      const response = await itemService.update(id, data)
      const index = items.value.findIndex(item => item.id === id)
      if (index !== -1) {
        items.value[index] = response.data
      }
      await fetchStats()
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to update item'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteItem(id) {
    loading.value = true
    error.value = null
    try {
      await itemService.delete(id)
      items.value = items.value.filter(item => item.id !== id)
      selectedItems.value = selectedItems.value.filter(itemId => itemId !== id)
      await fetchStats()
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to delete item'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function bulkDelete(ids) {
    loading.value = true
    error.value = null
    try {
      await itemService.bulkDelete(ids)
      items.value = items.value.filter(item => !ids.includes(item.id))
      selectedItems.value = []
      await fetchStats()
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to delete items'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function bulkUpdate(ids, data) {
    loading.value = true
    error.value = null
    try {
      await itemService.bulkUpdate(ids, data)
      items.value.forEach(item => {
        if (ids.includes(item.id)) {
          Object.assign(item, data)
        }
      })
      await fetchStats()
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to update items'
      throw err
    } finally {
      loading.value = false
    }
  }

  function setFilters(newFilters) {
    filters.value = { ...filters.value, ...newFilters }
  }

  function clearFilters() {
    filters.value = {
      category: '',
      priority: '',
      completed: '',
      due_filter: '',
      search: '',
    }
    sortBy.value = '-created_at'
  }

  function toggleSelection(itemId) {
    const index = selectedItems.value.indexOf(itemId)
    if (index > -1) {
      selectedItems.value.splice(index, 1)
    } else {
      selectedItems.value.push(itemId)
    }
  }

  function clearSelection() {
    selectedItems.value = []
  }

  function setError(message) {
    error.value = message
  }

  function clearError() {
    error.value = null
  }

  return {
    // State
    items,
    loading,
    error,
    filters,
    sortBy,
    selectedItems,
    stats,
    // Getters
    completedItems,
    pendingItems,
    overdueItems,
    filteredItems,
    hasActiveFilters,
    // Actions
    fetchItems,
    fetchStats,
    createItem,
    updateItem,
    deleteItem,
    bulkDelete,
    bulkUpdate,
    setFilters,
    clearFilters,
    toggleSelection,
    clearSelection,
    setError,
    clearError,
  }
})
