import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useFilters } from '../useFilters'
import { SORT_OPTIONS } from '../../utils/constants'

// Mock useDebounce
vi.mock('../useDebounce', () => ({
  useDebounce: vi.fn(value => ({ value })),
}))

describe('useFilters', () => {
  let filters

  beforeEach(() => {
    filters = useFilters()
  })

  describe('initial state', () => {
    it('should initialize with empty filters', () => {
      expect(filters.filters.category).toBe('')
      expect(filters.filters.priority).toBe('')
      expect(filters.filters.completed).toBe('')
      expect(filters.filters.due_filter).toBe('')
      expect(filters.filters.search).toBe('')
    })

    it('should initialize with default sort option', () => {
      expect(filters.sortBy.value).toBe(SORT_OPTIONS.NEWEST_FIRST)
    })
  })

  describe('hasActiveFilters', () => {
    it('should return false when no filters are active', () => {
      expect(filters.hasActiveFilters()).toBe(false)
    })

    it('should return true when category filter is active', () => {
      filters.filters.category = 'work'
      expect(filters.hasActiveFilters()).toBe(true)
    })

    it('should return true when priority filter is active', () => {
      filters.filters.priority = 'high'
      expect(filters.hasActiveFilters()).toBe(true)
    })

    it('should return true when completed filter is active', () => {
      filters.filters.completed = 'true'
      expect(filters.hasActiveFilters()).toBe(true)
    })

    it('should return true when due_filter is active', () => {
      filters.filters.due_filter = 'overdue'
      expect(filters.hasActiveFilters()).toBe(true)
    })

    it('should return true when search is active', () => {
      filters.filters.search = 'test'
      expect(filters.hasActiveFilters()).toBe(true)
    })

    it('should return true when sort is changed', () => {
      filters.sortBy.value = SORT_OPTIONS.OLDEST_FIRST
      expect(filters.hasActiveFilters()).toBe(true)
    })
  })

  describe('resetFilters', () => {
    it('should reset all filters to empty', () => {
      filters.filters.category = 'work'
      filters.filters.priority = 'high'
      filters.filters.completed = 'true'
      filters.filters.due_filter = 'overdue'
      filters.filters.search = 'test'
      filters.sortBy.value = SORT_OPTIONS.OLDEST_FIRST

      filters.resetFilters()

      expect(filters.filters.category).toBe('')
      expect(filters.filters.priority).toBe('')
      expect(filters.filters.completed).toBe('')
      expect(filters.filters.due_filter).toBe('')
      expect(filters.filters.search).toBe('')
      expect(filters.sortBy.value).toBe(SORT_OPTIONS.NEWEST_FIRST)
    })
  })

  describe('getDebouncedSearch', () => {
    it('should return debounced search value', () => {
      filters.filters.search = 'test query'
      const debounced = filters.getDebouncedSearch()
      expect(debounced).toBeDefined()
    })

    it('should accept custom delay', () => {
      filters.filters.search = 'test'
      const debounced = filters.getDebouncedSearch(500)
      expect(debounced).toBeDefined()
    })
  })

  describe('getFilterParams', () => {
    it('should return empty object when no filters are set', () => {
      const params = filters.getFilterParams()
      expect(params.category).toBeUndefined()
      expect(params.priority).toBeUndefined()
      expect(params.completed).toBeUndefined()
      expect(params.due_filter).toBeUndefined()
      expect(params.search).toBeUndefined()
    })

    it('should return filter params when filters are set', () => {
      filters.filters.category = 'work'
      filters.filters.priority = 'high'
      filters.filters.completed = 'true'
      filters.filters.due_filter = 'overdue'
      filters.filters.search = 'test'

      const params = filters.getFilterParams()

      expect(params.category).toBe('work')
      expect(params.priority).toBe('high')
      expect(params.completed).toBe('true')
      expect(params.due_filter).toBe('overdue')
      expect(params.search).toBe('test')
    })

    it('should exclude empty string values', () => {
      filters.filters.category = 'work'
      filters.filters.priority = ''
      filters.filters.search = 'test'

      const params = filters.getFilterParams()

      expect(params.category).toBe('work')
      expect(params.priority).toBeUndefined()
      expect(params.search).toBe('test')
    })
  })
})
