/**
 * Composable for infinite scroll functionality
 * Implements Single Responsibility Principle - handles only scroll detection
 * 
 * @param {Function} onLoadMore - Callback function when scroll reaches threshold
 * @param {Object} options - Configuration options
 * @returns {Object} - Reactive refs and methods for infinite scroll
 */
export function useInfiniteScroll(onLoadMore, options = {}) {
  const {
    rootMargin = '100px',
    threshold = 0.1,
    root = null
  } = options

  let observer = null
  const loadMoreTriggerRef = { value: null }

  const setupObserver = (element) => {
    if (!element || !window.IntersectionObserver) {
      return
    }

    const observerOptions = {
      root,
      rootMargin,
      threshold
    }

    observer = new IntersectionObserver((entries) => {
      const entry = entries[0]
      if (entry?.isIntersecting) {
        onLoadMore()
      }
    }, observerOptions)

    observer.observe(element)
  }

  const disconnect = () => {
    if (observer) {
      observer.disconnect()
      observer = null
    }
  }

  const observe = (element) => {
    disconnect()
    if (element) {
      loadMoreTriggerRef.value = element
      setupObserver(element)
    }
  }

  return {
    loadMoreTriggerRef,
    observe,
    disconnect
  }
}
