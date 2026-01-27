import { describe, it, expect, beforeEach } from 'vitest'
import { usePagination } from '../usePagination'

describe('usePagination', () => {
  let pagination

  beforeEach(() => {
    pagination = usePagination()
  })

  describe('initial state', () => {
    it('should initialize with default values', () => {
      expect(pagination.pagination.currentPage).toBe(1)
      expect(pagination.pagination.totalPages).toBe(1)
      expect(pagination.pagination.totalCount).toBe(0)
      expect(pagination.pagination.hasNext).toBe(false)
      expect(pagination.pagination.hasPrevious).toBe(false)
    })
  })

  describe('updatePagination', () => {
    it('should update pagination from paginated response', () => {
      const response = {
        results: [{ id: 1 }, { id: 2 }],
        count: 20,
        next: 'http://example.com/api/items/?page=2',
        previous: null,
      }

      pagination.pagination.currentPage = 1
      pagination.updatePagination(response)

      expect(pagination.pagination.totalCount).toBe(20)
      expect(pagination.pagination.hasNext).toBe(true)
      expect(pagination.pagination.hasPrevious).toBe(false)
    })

    it('should handle response without next/previous', () => {
      const response = {
        results: [{ id: 1 }],
        count: 1,
        next: null,
        previous: null,
      }

      pagination.updatePagination(response)

      expect(pagination.pagination.hasNext).toBe(false)
      expect(pagination.pagination.hasPrevious).toBe(false)
    })

    it('should handle array response (non-paginated)', () => {
      const response = [{ id: 1 }, { id: 2 }, { id: 3 }]

      pagination.updatePagination(response)

      expect(pagination.pagination.totalCount).toBe(3)
      expect(pagination.pagination.currentPage).toBe(1)
      expect(pagination.pagination.totalPages).toBe(1)
      expect(pagination.pagination.hasNext).toBe(false)
    })

    it('should reset pagination for invalid response', () => {
      pagination.pagination.currentPage = 5
      pagination.pagination.totalCount = 100

      pagination.updatePagination(null)
      pagination.updatePagination({})

      expect(pagination.pagination.currentPage).toBe(1)
      expect(pagination.pagination.totalCount).toBe(0)
    })
  })

  describe('resetPagination', () => {
    it('should reset all pagination values', () => {
      pagination.pagination.currentPage = 5
      pagination.pagination.totalPages = 10
      pagination.pagination.totalCount = 100
      pagination.pagination.hasNext = true
      pagination.pagination.hasPrevious = true

      pagination.resetPagination()

      expect(pagination.pagination.currentPage).toBe(1)
      expect(pagination.pagination.totalPages).toBe(1)
      expect(pagination.pagination.totalCount).toBe(0)
      expect(pagination.pagination.hasNext).toBe(false)
      expect(pagination.pagination.hasPrevious).toBe(false)
    })
  })

  describe('goToPage', () => {
    beforeEach(() => {
      pagination.pagination.totalPages = 5
    })

    it('should navigate to valid page', () => {
      const result = pagination.goToPage(3)
      expect(result).toBe(true)
      expect(pagination.pagination.currentPage).toBe(3)
    })

    it('should not navigate to page less than 1', () => {
      const result = pagination.goToPage(0)
      expect(result).toBe(false)
      expect(pagination.pagination.currentPage).toBe(1)
    })

    it('should not navigate to page greater than totalPages', () => {
      const result = pagination.goToPage(10)
      expect(result).toBe(false)
      expect(pagination.pagination.currentPage).toBe(1)
    })

    it('should normalize invalid page numbers', () => {
      pagination.goToPage('invalid')
      expect(pagination.pagination.currentPage).toBe(1)
    })
  })

  describe('nextPage', () => {
    it('should go to next page when available', () => {
      pagination.pagination.currentPage = 1
      pagination.pagination.totalPages = 3
      pagination.pagination.hasNext = true

      const result = pagination.nextPage()

      expect(result).toBe(true)
      expect(pagination.pagination.currentPage).toBe(2)
    })

    it('should not go to next page when not available', () => {
      pagination.pagination.currentPage = 3
      pagination.pagination.totalPages = 3
      pagination.pagination.hasNext = false

      const result = pagination.nextPage()

      expect(result).toBe(false)
      expect(pagination.pagination.currentPage).toBe(3)
    })
  })

  describe('previousPage', () => {
    it('should go to previous page when available', () => {
      pagination.pagination.currentPage = 2
      pagination.pagination.hasPrevious = true

      const result = pagination.previousPage()

      expect(result).toBe(true)
      expect(pagination.pagination.currentPage).toBe(1)
    })

    it('should not go to previous page when on first page', () => {
      pagination.pagination.currentPage = 1
      pagination.pagination.hasPrevious = false

      const result = pagination.previousPage()

      expect(result).toBe(false)
      expect(pagination.pagination.currentPage).toBe(1)
    })
  })

  describe('resetToFirstPage', () => {
    it('should reset to first page', () => {
      pagination.pagination.currentPage = 5
      pagination.resetToFirstPage()
      expect(pagination.pagination.currentPage).toBe(1)
    })
  })
})
