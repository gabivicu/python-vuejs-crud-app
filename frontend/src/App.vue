<template>
  <div :class="['min-h-screen bg-background', { dark: darkMode }]">
    <!-- Router View -->
    <router-view
      :show-dashboard="showDashboard"
      :create-modal-trigger="createModalTrigger"
      @update:create-modal-trigger="createModalTrigger = $event"
    />
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      darkMode: localStorage.getItem('darkMode') === 'true',
      showDashboard: false,
      createModalTrigger: 0,
    }
  },
  mounted() {
    if (this.darkMode) {
      document.documentElement.classList.add('dark')
    }
  },
  methods: {
    toggleDarkMode() {
      this.darkMode = !this.darkMode
      localStorage.setItem('darkMode', this.darkMode)
      if (this.darkMode) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    },
    toggleDashboard() {
      this.showDashboard = !this.showDashboard
    },
    triggerCreateModal() {
      // Trigger modal opening by incrementing the counter
      this.createModalTrigger++
    },
  },
}
</script>

<style>
/* Global styles are in style.css */
</style>
