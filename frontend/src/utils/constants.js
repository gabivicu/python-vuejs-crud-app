/**
 * Application-wide constants
 * Centralized configuration following DRY principle
 */

export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 10,
  INITIAL_PAGE: 1,
  MIN_PAGE: 1
}

export const ITEM_CATEGORIES = {
  WORK: 'work',
  PERSONAL: 'personal',
  SHOPPING: 'shopping',
  HEALTH: 'health',
  FINANCE: 'finance',
  OTHER: 'other'
}

export const ITEM_PRIORITIES = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  URGENT: 'urgent'
}

export const ITEM_STATUS = {
  COMPLETED: 'completed',
  PENDING: 'pending'
}

export const SORT_OPTIONS = {
  NEWEST_FIRST: '-created_at',
  OLDEST_FIRST: 'created_at',
  DUE_DATE: 'due_date',
  PRIORITY: '-priority',
  TITLE_AZ: 'title'
}

export const DATE_FILTERS = {
  OVERDUE: 'overdue',
  TODAY: 'today',
  UPCOMING: 'upcoming'
}

export const MONTHS = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
]

export const WEEK_DAYS = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']

export const CALENDAR_CONFIG = {
  YEAR_RANGE_START_OFFSET: 5,
  YEAR_RANGE_END_OFFSET: 6,
  CALENDAR_GRID_SIZE: 42 // 6 weeks * 7 days
}
