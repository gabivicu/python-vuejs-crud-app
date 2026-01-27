import { PAGINATION } from './constants'

/**
 * Validates if a page number is valid
 * @param {number} page - Page number to validate
 * @returns {boolean} - True if valid
 */
export function isValidPage(page) {
  return (
    typeof page === 'number' &&
    !isNaN(page) &&
    isFinite(page) &&
    page >= PAGINATION.MIN_PAGE
  )
}

/**
 * Normalizes a page number to a valid value
 * @param {number} page - Page number to normalize
 * @returns {number} - Normalized page number
 */
export function normalizePage(page) {
  if (!isValidPage(page)) {
    return PAGINATION.INITIAL_PAGE
  }
  return page
}

/**
 * Validates pagination response structure
 * @param {Object} response - API response
 * @returns {boolean} - True if valid pagination response
 */
export function isValidPaginationResponse(response) {
  return (
    response &&
    typeof response === 'object' &&
    Array.isArray(response.results) &&
    typeof response.count === 'number'
  )
}
