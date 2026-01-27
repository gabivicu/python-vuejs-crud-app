<template>
  <div :class="['app-container', { 'dark-mode': darkMode }]">
    <!-- Header with Hamburger Menu (hidden on landing page) -->
    <div v-if="$route.path !== '/'" class="container">
      <div class="header">
        <div class="header-left">
          <HamburgerMenu />
          <h1>📝 Todo Items</h1>
          <button
            class="btn btn-icon"
            :title="darkMode ? 'Light Mode' : 'Dark Mode'"
            @click="toggleDarkMode"
          >
            {{ darkMode ? '☀️' : '🌙' }}
          </button>
        </div>
        <div v-if="$route.path === '/app'" class="header-actions">
          <button class="btn btn-secondary" @click="toggleDashboard">📊 Dashboard</button>
          <button class="btn btn-primary" @click="triggerCreateModal">+ Add New Item</button>
        </div>
      </div>
    </div>

    <!-- Router View -->
    <div :class="{ container: $route.path !== '/' }">
      <router-view
        :show-dashboard="showDashboard"
        :create-modal-trigger="createModalTrigger"
        @update:create-modal-trigger="createModalTrigger = $event"
      />
    </div>
  </div>
</template>

<script>
import HamburgerMenu from './components/HamburgerMenu.vue'

export default {
  name: 'App',
  components: {
    HamburgerMenu,
  },
  data() {
    return {
      darkMode: localStorage.getItem('darkMode') === 'true',
      showDashboard: false,
      createModalTrigger: 0,
    }
  },
  mounted() {
    if (this.darkMode) {
      document.body.classList.add('dark-mode')
    }
  },
  methods: {
    toggleDarkMode() {
      this.darkMode = !this.darkMode
      localStorage.setItem('darkMode', this.darkMode)
      if (this.darkMode) {
        document.body.classList.add('dark-mode')
      } else {
        document.body.classList.remove('dark-mode')
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
