import { reactive } from 'vue'
import { PAGINATION } from '../utils/constants'
import { normalizePage } from '../utils/validators'

export function usePagination() {
  const pagination = reactive({
    currentPage: PAGINATION.INITIAL_PAGE,
    totalPages: 1,
    totalCount: 0,
    pageSize: PAGINATION.DEFAULT_PAGE_SIZE,
    hasNext: false,
    hasPrevious: false,
  })

  const updatePagination = response => {
    if (!response || typeof response !== 'object') {
      return resetPagination()
    }

    if (Array.isArray(response.results)) {
      // Paginated response
      const count = response.count || 0
      const nextUrl = response.next
      const previousUrl = response.previous
      const totalPages = Math.ceil(count / pagination.pageSize)
      const currentPage = normalizePage(pagination.currentPage)

      Object.assign(pagination, {
        currentPage,
        totalPages,
        totalCount: count,
        hasNext: !!nextUrl,
        hasPrevious: !!previousUrl,
      })
    } else if (Array.isArray(response)) {
      // Non-paginated array response
      Object.assign(pagination, {
        currentPage: PAGINATION.INITIAL_PAGE,
        totalPages: 1,
        totalCount: response.length,
        pageSize: response.length,
        hasNext: false,
        hasPrevious: false,
      })
    } else {
      resetPagination()
    }
  }

  const resetPagination = () => {
    Object.assign(pagination, {
      currentPage: PAGINATION.INITIAL_PAGE,
      totalPages: 1,
      totalCount: 0,
      pageSize: PAGINATION.DEFAULT_PAGE_SIZE,
      hasNext: false,
      hasPrevious: false,
    })
  }

  const goToPage = page => {
    const normalizedPage = normalizePage(page)
    if (normalizedPage >= PAGINATION.MIN_PAGE && normalizedPage <= pagination.totalPages) {
      pagination.currentPage = normalizedPage
      return true
    }
    return false
  }

  const nextPage = () => {
    if (pagination.hasNext && pagination.currentPage < pagination.totalPages) {
      pagination.currentPage++
      return true
    }
    return false
  }

  const previousPage = () => {
    if (pagination.hasPrevious && pagination.currentPage > PAGINATION.MIN_PAGE) {
      pagination.currentPage--
      return true
    }
    return false
  }

  const resetToFirstPage = () => {
    pagination.currentPage = PAGINATION.INITIAL_PAGE
  }

  return {
    pagination,
    updatePagination,
    resetPagination,
    goToPage,
    nextPage,
    previousPage,
    resetToFirstPage,
  }
}
