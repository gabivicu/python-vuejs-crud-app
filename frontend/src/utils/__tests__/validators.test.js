import { describe, it, expect } from 'vitest'
import { isValidPage, normalizePage, isValidPaginationResponse } from '../validators'

describe('validators', () => {
  describe('isValidPage', () => {
    it('should return true for valid page numbers', () => {
      expect(isValidPage(1)).toBe(true)
      expect(isValidPage(5)).toBe(true)
      expect(isValidPage(100)).toBe(true)
    })

    it('should return false for negative numbers', () => {
      expect(isValidPage(-1)).toBe(false)
      expect(isValidPage(-10)).toBe(false)
    })

    it('should return false for zero', () => {
      expect(isValidPage(0)).toBe(false)
    })

    it('should return false for non-numbers', () => {
      expect(isValidPage('1')).toBe(false)
      expect(isValidPage(null)).toBe(false)
      expect(isValidPage(undefined)).toBe(false)
      expect(isValidPage({})).toBe(false)
      expect(isValidPage([])).toBe(false)
    })

    it('should return false for NaN', () => {
      expect(isValidPage(NaN)).toBe(false)
    })

    it('should return false for Infinity', () => {
      expect(isValidPage(Infinity)).toBe(false)
      expect(isValidPage(-Infinity)).toBe(false)
    })
  })

  describe('normalizePage', () => {
    it('should return the page number if valid', () => {
      expect(normalizePage(1)).toBe(1)
      expect(normalizePage(5)).toBe(5)
      expect(normalizePage(100)).toBe(100)
    })

    it('should return initial page for invalid values', () => {
      expect(normalizePage(-1)).toBe(1)
      expect(normalizePage(0)).toBe(1)
      expect(normalizePage('1')).toBe(1)
      expect(normalizePage(null)).toBe(1)
      expect(normalizePage(undefined)).toBe(1)
      expect(normalizePage(NaN)).toBe(1)
    })
  })

  describe('isValidPaginationResponse', () => {
    it('should return true for valid pagination response', () => {
      const response = {
        results: [{ id: 1 }, { id: 2 }],
        count: 2,
        next: null,
        previous: null,
      }
      expect(isValidPaginationResponse(response)).toBe(true)
    })

    it('should return false for non-object', () => {
      expect(isValidPaginationResponse(null)).toBe(false)
      expect(isValidPaginationResponse(undefined)).toBe(false)
      expect(isValidPaginationResponse('string')).toBe(false)
      expect(isValidPaginationResponse(123)).toBe(false)
      expect(isValidPaginationResponse([])).toBe(false)
    })

    it('should return false for missing results array', () => {
      const response = {
        count: 2,
      }
      expect(isValidPaginationResponse(response)).toBe(false)
    })

    it('should return false for non-array results', () => {
      const response = {
        results: {},
        count: 2,
      }
      expect(isValidPaginationResponse(response)).toBe(false)
    })

    it('should return false for missing count', () => {
      const response = {
        results: [{ id: 1 }],
      }
      expect(isValidPaginationResponse(response)).toBe(false)
    })

    it('should return false for non-number count', () => {
      const response = {
        results: [{ id: 1 }],
        count: '2',
      }
      expect(isValidPaginationResponse(response)).toBe(false)
    })

    it('should return true even with empty results array', () => {
      const response = {
        results: [],
        count: 0,
      }
      expect(isValidPaginationResponse(response)).toBe(true)
    })
  })
})
