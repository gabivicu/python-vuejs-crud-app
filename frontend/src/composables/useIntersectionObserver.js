import { onMounted, onUnmounted, ref } from 'vue'

export function useIntersectionObserver(callback, options = {}) {
  const targetRef = ref(null)
  let observer = null

  onMounted(() => {
    if (!window.IntersectionObserver) return

    observer = new IntersectionObserver(entries => {
      const entry = entries[0]
      if (entry && entry.isIntersecting) {
        callback()
      }
    }, options)

    if (targetRef.value) {
      observer.observe(targetRef.value)
    }
  })

  onUnmounted(() => {
    if (observer) {
      observer.disconnect()
    }
  })

  return {
    targetRef,
  }
}
