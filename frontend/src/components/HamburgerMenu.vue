<template>
  <div class="hamburger-menu">
    <button
      class="hamburger-btn"
      :class="{ active: isOpen }"
      aria-label="Toggle menu"
      @click="toggleMenu"
    >
      <span></span>
      <span></span>
      <span></span>
    </button>

    <div :class="['sidebar', { open: isOpen }]" @click.stop>
      <div class="sidebar-header">
        <h2>📝 Menu</h2>
        <button class="close-sidebar-btn" @click="toggleMenu">&times;</button>
      </div>
      <nav class="sidebar-nav">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: $route.path === item.path }"
          @click="closeMenu"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-label">{{ item.label }}</span>
        </router-link>
      </nav>
    </div>

    <div v-if="isOpen" class="sidebar-overlay" @click="closeMenu"></div>
  </div>
</template>

<script>
export default {
  name: 'HamburgerMenu',
  data() {
    return {
      isOpen: false,
      menuItems: [
        { path: '/', label: 'Landing', icon: '🚀' },
        { path: '/app', label: 'My Tasks', icon: '📝' },
        { path: '/about', label: 'About', icon: 'ℹ️' },
        { path: '/settings', label: 'Settings', icon: '⚙️' },
      ],
    }
  },
  watch: {
    $route() {
      // Close menu when route changes
      this.closeMenu()
    },
  },
  beforeUnmount() {
    document.body.style.overflow = ''
  },
  methods: {
    toggleMenu() {
      this.isOpen = !this.isOpen
      if (this.isOpen) {
        document.body.style.overflow = 'hidden'
      } else {
        document.body.style.overflow = ''
      }
    },
    closeMenu() {
      this.isOpen = false
      document.body.style.overflow = ''
    },
  },
}
</script>

<style scoped>
.hamburger-menu {
  position: relative;
}

.hamburger-btn {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  width: 30px;
  height: 30px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 1001;
  transition: all 0.3s ease;
}

.hamburger-btn span {
  width: 100%;
  height: 3px;
  background: var(--text-primary);
  border-radius: 3px;
  transition: all 0.3s ease;
  transform-origin: center;
}

.hamburger-btn.active span:nth-child(1) {
  transform: rotate(45deg) translate(8px, 8px);
}

.hamburger-btn.active span:nth-child(2) {
  opacity: 0;
}

.hamburger-btn.active span:nth-child(3) {
  transform: rotate(-45deg) translate(8px, -8px);
}

.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.sidebar {
  position: fixed;
  top: 0;
  left: -300px;
  width: 300px;
  height: 100vh;
  background: var(--bg-primary);
  box-shadow: 2px 0 10px var(--shadow);
  z-index: 1000;
  transition: left 0.3s ease;
  overflow-y: auto;
}

.sidebar.open {
  left: 0;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid var(--border-color);
}

.sidebar-header h2 {
  margin: 0;
  color: var(--text-primary);
  font-size: 1.5rem;
}

.close-sidebar-btn {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: var(--text-secondary);
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s ease;
}

.close-sidebar-btn:hover {
  color: var(--text-primary);
}

.sidebar-nav {
  padding: 20px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px 20px;
  color: var(--text-primary);
  text-decoration: none;
  transition: all 0.2s ease;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background: var(--bg-secondary);
  border-left-color: var(--primary);
}

.nav-item.active {
  background: var(--bg-tertiary);
  border-left-color: var(--primary);
  font-weight: 600;
}

.nav-icon {
  font-size: 20px;
  width: 24px;
  text-align: center;
}

.nav-label {
  font-size: 16px;
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    width: 280px;
  }
}
</style>
