<template>
  <div :class="['app-container', { 'dark-mode': darkMode }]">
    <div class="container">
      <!-- Header with Hamburger Menu -->
      <div class="header">
        <div class="header-left">
          <HamburgerMenu />
          <h1>📝 Todo Items</h1>
          <button @click="toggleDarkMode" class="btn btn-icon" :title="darkMode ? 'Light Mode' : 'Dark Mode'">
            {{ darkMode ? '☀️' : '🌙' }}
          </button>
        </div>
        <div class="header-actions" v-if="$route.path === '/'">
          <button @click="toggleDashboard" class="btn btn-secondary">
            📊 Dashboard
          </button>
          <button @click="triggerCreateModal" class="btn btn-primary">
            + Add New Item
          </button>
        </div>
      </div>

      <!-- Router View -->
      <router-view 
        :showDashboard="showDashboard"
        ref="routerView"
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
      // Call openCreateModal on Home component if it exists
      if (this.$refs.routerView && this.$refs.routerView.openCreateModal) {
        this.$refs.routerView.openCreateModal()
      }
    },
  },
}
</script>

<style>
/* Global styles are in style.css */
</style>
