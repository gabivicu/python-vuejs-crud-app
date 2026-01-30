<template>
  <div class="min-h-screen bg-background text-foreground">
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
      showDashboard: false,
      createModalTrigger: 0,
    }
  },
  methods: {
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
