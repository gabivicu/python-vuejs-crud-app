import { describe, it, expect } from 'vitest'
import {
  formatDate,
  formatDisplayDate,
  formatDateForInput,
  isOverdue,
  getPriorityLabel,
  getCategoryLabel,
} from '../formatters'

describe('formatters', () => {
  describe('formatDate', () => {
    it('should format a valid date string', () => {
      const dateString = '2024-01-15T10:30:00Z'
      const formatted = formatDate(dateString)
      expect(formatted).toBeTruthy()
      expect(typeof formatted).toBe('string')
    })

    it('should return empty string for null', () => {
      expect(formatDate(null)).toBe('')
    })

    it('should return empty string for undefined', () => {
      expect(formatDate(undefined)).toBe('')
    })

    it('should return empty string for empty string', () => {
      expect(formatDate('')).toBe('')
    })
  })

  describe('formatDisplayDate', () => {
    it('should format date for display', () => {
      const dateString = '2024-01-15T10:30:00Z'
      const formatted = formatDisplayDate(dateString)
      expect(formatted).toContain('15')
      expect(formatted).toContain('2024')
    })

    it('should return empty string for null', () => {
      expect(formatDisplayDate(null)).toBe('')
    })

    it('should return empty string for empty string', () => {
      expect(formatDisplayDate('')).toBe('')
    })
  })

  describe('formatDateForInput', () => {
    it('should format date to YYYY-MM-DD', () => {
      const date = new Date('2024-01-15T10:30:00Z')
      const formatted = formatDateForInput(date)
      expect(formatted).toMatch(/^\d{4}-\d{2}-\d{2}$/)
      expect(formatted).toBe('2024-01-15')
    })

    it('should format date string to YYYY-MM-DD', () => {
      const formatted = formatDateForInput('2024-01-15T10:30:00Z')
      expect(formatted).toBe('2024-01-15')
    })

    it('should return empty string for null', () => {
      expect(formatDateForInput(null)).toBe('')
    })

    it('should pad single digit months and days', () => {
      const date = new Date('2024-01-05T10:30:00Z')
      const formatted = formatDateForInput(date)
      expect(formatted).toBe('2024-01-05')
    })
  })

  describe('isOverdue', () => {
    it('should return true for past dates when not completed', () => {
      const pastDate = new Date(Date.now() - 86400000).toISOString() // Yesterday
      expect(isOverdue(pastDate, false)).toBe(true)
    })

    it('should return false for future dates', () => {
      const futureDate = new Date(Date.now() + 86400000).toISOString() // Tomorrow
      expect(isOverdue(futureDate, false)).toBe(false)
    })

    it('should return false for completed items even if overdue', () => {
      const pastDate = new Date(Date.now() - 86400000).toISOString()
      expect(isOverdue(pastDate, true)).toBe(false)
    })

    it('should return false for null due date', () => {
      expect(isOverdue(null, false)).toBe(false)
    })

    it('should return false for empty string due date', () => {
      expect(isOverdue('', false)).toBe(false)
    })
  })

  describe('getPriorityLabel', () => {
    it('should return correct label for low priority', () => {
      expect(getPriorityLabel('low')).toBe('Low')
    })

    it('should return correct label for medium priority', () => {
      expect(getPriorityLabel('medium')).toBe('Medium')
    })

    it('should return correct label for high priority', () => {
      expect(getPriorityLabel('high')).toBe('High')
    })

    it('should return correct label for urgent priority', () => {
      expect(getPriorityLabel('urgent')).toBe('Urgent')
    })

    it('should return default label for unknown priority', () => {
      expect(getPriorityLabel('unknown')).toBe('Medium')
    })

    it('should return default label for undefined', () => {
      expect(getPriorityLabel(undefined)).toBe('Medium')
    })
  })

  describe('getCategoryLabel', () => {
    it('should return correct label for work category', () => {
      expect(getCategoryLabel('work')).toBe('Work')
    })

    it('should return correct label for personal category', () => {
      expect(getCategoryLabel('personal')).toBe('Personal')
    })

    it('should return correct label for shopping category', () => {
      expect(getCategoryLabel('shopping')).toBe('Shopping')
    })

    it('should return correct label for health category', () => {
      expect(getCategoryLabel('health')).toBe('Health')
    })

    it('should return correct label for finance category', () => {
      expect(getCategoryLabel('finance')).toBe('Finance')
    })

    it('should return correct label for other category', () => {
      expect(getCategoryLabel('other')).toBe('Other')
    })

    it('should return default label for unknown category', () => {
      expect(getCategoryLabel('unknown')).toBe('Other')
    })

    it('should return default label for undefined', () => {
      expect(getCategoryLabel(undefined)).toBe('Other')
    })
  })
})
