/**
 * Pure utility functions for data formatting
 * Follows Single Responsibility Principle - each function has one purpose
 */

import { MONTHS } from './constants'

/**
 * Formats a date string to a readable format
 * @param {string} dateString - ISO date string
 * @returns {string} - Formatted date string
 */
export function formatDate(dateString) {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

/**
 * Formats a date for display in calendar
 * @param {string} dateString - ISO date string
 * @returns {string} - Formatted date string (e.g., "15 January 2024")
 */
export function formatDisplayDate(dateString) {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  const day = date.getDate()
  const month = MONTHS[date.getMonth()]
  const year = date.getFullYear()
  
  return `${day} ${month} ${year}`
}

/**
 * Formats a date string to YYYY-MM-DD format
 * @param {Date|string} date - Date object or string
 * @returns {string} - Formatted date string
 */
export function formatDateForInput(date) {
  if (!date) return ''
  
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  
  return `${year}-${month}-${day}`
}

/**
 * Checks if a date is overdue
 * @param {string} dueDate - ISO date string
 * @param {boolean} isCompleted - Whether the item is completed
 * @returns {boolean} - True if overdue
 */
export function isOverdue(dueDate, isCompleted) {
  if (!dueDate || isCompleted) return false
  return new Date(dueDate) < new Date()
}

/**
 * Gets priority label
 * @param {string} priority - Priority value
 * @returns {string} - Human-readable priority label
 */
export function getPriorityLabel(priority) {
  const labels = {
    low: 'Low',
    medium: 'Medium',
    high: 'High',
    urgent: 'Urgent',
  }
  return labels[priority] || 'Medium'
}

/**
 * Gets category label
 * @param {string} category - Category value
 * @returns {string} - Human-readable category label
 */
export function getCategoryLabel(category) {
  const labels = {
    work: 'Work',
    personal: 'Personal',
    shopping: 'Shopping',
    health: 'Health',
    finance: 'Finance',
    other: 'Other',
  }
  return labels[category] || 'Other'
}
