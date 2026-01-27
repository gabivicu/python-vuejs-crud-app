import { SORT_OPTIONS, ITEM_CATEGORIES, ITEM_PRIORITIES, DATE_FILTERS } from '../utils/constants'
import { useDebounce } from './useDebounce'

export function useFilters() {
  const filters = {
    category: '',
    priority: '',
    completed: '',
    due_filter: '',
    search: ''
  }

  const sortBy = { value: SORT_OPTIONS.NEWEST_FIRST }

  /**
   * Checks if any filters are active
   * @returns {boolean} - True if any filter is active
   */
  const hasActiveFilters = () => {
    return (
      Object.values(filters).some(v => v !== '') ||
      sortBy.value !== SORT_OPTIONS.NEWEST_FIRST
    )
  }

  /**
   * Resets all filters to default values
   */
  const resetFilters = () => {
    filters.category = ''
    filters.priority = ''
    filters.completed = ''
    filters.due_filter = ''
    filters.search = ''
    sortBy.value = SORT_OPTIONS.NEWEST_FIRST
  }

  /**
   * Gets debounced search query
   * @param {number} delay - Debounce delay in milliseconds
   * @returns {Object} - Debounced value ref
   */
  const getDebouncedSearch = (delay = 300) => {
    return useDebounce(filters.search, delay)
  }

  /**
   * Builds filter object for API requests
   * @returns {Object} - Filter object
   */
  const getFilterParams = () => {
    return {
      category: filters.category || undefined,
      priority: filters.priority || undefined,
      completed: filters.completed || undefined,
      due_filter: filters.due_filter || undefined,
      search: filters.search || undefined
    }
  }

  return {
    filters,
    sortBy,
    hasActiveFilters,
    resetFilters,
    getDebouncedSearch,
    getFilterParams
  }
}
