import { ref } from 'vue'
import { itemService } from '../api'
import { usePagination } from './usePagination'
import { isValidPaginationResponse } from '../utils/validators'

export function useItems() {
  const items = ref([])
  const loading = ref(false)
  const error = ref(null)

  const { pagination, updatePagination, resetPagination, resetToFirstPage } = usePagination()

  /**
   * Builds query parameters from filters and sort options
   * @param {Object} filters - Filter options
   * @param {string} sortBy - Sort option
   * @param {number} page - Page number
   * @returns {Object} - Query parameters
   */
  const buildQueryParams = (filters, sortBy, page) => {
    const params = {
      ordering: sortBy,
    }

    // Only add page if greater than 1 (page 1 is default)
    if (page > 1) {
      params.page = page
    }

    // Add filters
    if (filters.category) params.category = filters.category
    if (filters.priority) params.priority = filters.priority
    if (filters.completed) params.completed = filters.completed
    if (filters.due_filter) params.due_filter = filters.due_filter
    if (filters.search) params.search = filters.search

    return params
  }

  /**
   * Fetches items from API
   * @param {Object} options - Fetch options
   * @param {Object} options.filters - Filter options
   * @param {string} options.sortBy - Sort option
   * @param {boolean} options.append - Whether to append to existing items
   * @returns {Promise<void>}
   */
  const fetchItems = async ({ filters = {}, sortBy = '-created_at', append = false }) => {
    loading.value = true
    error.value = null

    try {
      const currentPage = append ? pagination.currentPage : 1
      const params = buildQueryParams(filters, sortBy, currentPage)

      const response = await itemService.getAll(params)
      const responseData = response.data

      if (isValidPaginationResponse(responseData)) {
        // Handle paginated response
        if (append && currentPage > 1) {
          // Append new items, avoiding duplicates
          const newItems = responseData.results.filter(
            newItem => !items.value.some(existingItem => existingItem.id === newItem.id)
          )
          items.value.push(...newItems)
        } else {
          // Replace items for first page or when not appending
          items.value = [...responseData.results]
        }

        updatePagination(responseData)
      } else if (Array.isArray(responseData)) {
        // Non-paginated array response
        items.value = [...responseData]
        updatePagination(responseData)
      } else {
        throw new Error('Invalid response format')
      }
    } catch (err) {
      error.value = handleFetchError(err)
      items.value = []
      resetPagination()
    } finally {
      loading.value = false
    }
  }

  /**
   * Handles fetch errors and returns user-friendly messages
   * @param {Error} err - Error object
   * @returns {string} - Error message
   */
  const handleFetchError = err => {
    if (err.code === 'ECONNREFUSED' || err.message?.includes('Network Error')) {
      return 'Cannot connect to Django server. Please make sure it is running on http://localhost:8000'
    }

    if (err.response?.status === 404) {
      return 'API endpoint not found. Please check if the Django server is running and the API is accessible.'
    }

    if (err.response?.status >= 500) {
      return 'Server error. Please check the Django server logs.'
    }

    return err.response?.data?.detail || err.message || 'Failed to fetch items'
  }

  /**
   * Loads more items (for infinite scroll)
   * @param {Object} options - Fetch options
   * @returns {Promise<void>}
   */
  const loadMore = async options => {
    if (loading.value || !pagination.hasNext) {
      return
    }

    pagination.currentPage++
    await fetchItems({ ...options, append: true })
  }

  /**
   * Refreshes items list
   * @param {Object} options - Fetch options
   * @returns {Promise<void>}
   */
  const refreshItems = async options => {
    resetToFirstPage()
    await fetchItems({ ...options, append: false })
  }

  /**
   * Toggles item completion status
   * @param {Object} item - Item object
   * @returns {Promise<void>}
   */
  const toggleItemComplete = async item => {
    try {
      await itemService.patch(item.id, {
        completed: !item.completed,
      })
      // Update local state
      const itemIndex = items.value.findIndex(i => i.id === item.id)
      if (itemIndex !== -1) {
        items.value[itemIndex].completed = !item.completed
      }
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Failed to update item')
    }
  }

  /**
   * Deletes an item
   * @param {number} itemId - Item ID
   * @returns {Promise<void>}
   */
  const deleteItem = async itemId => {
    try {
      await itemService.delete(itemId)
      const index = items.value.findIndex(item => item.id === itemId)
      if (index !== -1) {
        items.value.splice(index, 1)
      }
    } catch (err) {
      throw new Error(err.response?.data?.detail || 'Failed to delete item')
    }
  }

  /**
   * Bulk operations
   */
  const bulkComplete = async itemIds => {
    try {
      await itemService.bulkUpdate(itemIds, { completed: true })
      itemIds.forEach(id => {
        const item = items.value.find(i => i.id === id)
        if (item) item.completed = true
      })
    } catch (err) {
      throw new Error('Failed to update items')
    }
  }

  const bulkDelete = async itemIds => {
    try {
      await itemService.bulkDelete(itemIds)
      itemIds.forEach(id => {
        const index = items.value.findIndex(item => item.id === id)
        if (index !== -1) items.value.splice(index, 1)
      })
    } catch (err) {
      throw new Error('Failed to delete items')
    }
  }

  return {
    items,
    loading,
    error,
    pagination,
    fetchItems,
    loadMore,
    refreshItems,
    toggleItemComplete,
    deleteItem,
    bulkComplete,
    bulkDelete,
  }
}
