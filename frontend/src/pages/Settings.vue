<template>
  <div class="page-content">
    <div class="page-header">
      <h1>⚙️ Settings</h1>
    </div>

    <div class="settings-content">
      <section class="settings-section">
        <h2>Appearance</h2>
        <div class="setting-item">
          <div class="setting-info">
            <label>Dark Mode</label>
            <p class="setting-description">Toggle between light and dark theme</p>
          </div>
          <button class="btn btn-secondary" @click="toggleDarkMode">
            {{ darkMode ? '☀️ Light Mode' : '🌙 Dark Mode' }}
          </button>
        </div>
      </section>

      <section class="settings-section">
        <h2>Data Management</h2>
        <div class="setting-item">
          <div class="setting-info">
            <label>Export Data</label>
            <p class="setting-description">Download your data as JSON or CSV</p>
          </div>
          <div class="setting-actions">
            <button class="btn btn-secondary btn-small" @click="exportAllJSON">Export JSON</button>
            <button class="btn btn-secondary btn-small" @click="exportAllCSV">Export CSV</button>
          </div>
        </div>
      </section>

      <section class="settings-section">
        <h2>Application Info</h2>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">Version</span>
            <span class="info-value">1.0.0</span>
          </div>
          <div class="info-item">
            <span class="info-label">Backend</span>
            <span class="info-value">Django 4.2.7</span>
          </div>
          <div class="info-item">
            <span class="info-label">Frontend</span>
            <span class="info-value">Vue.js 3</span>
          </div>
          <div class="info-item">
            <span class="info-label">Database</span>
            <span class="info-value">SQLite</span>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import { itemService } from '../api'

export default {
  name: 'Settings',
  data() {
    return {
      darkMode: localStorage.getItem('darkMode') === 'true',
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
    async exportAllJSON() {
      try {
        const response = await itemService.getAll()
        const items = response.data.results || response.data
        const dataStr = JSON.stringify(items, null, 2)
        const dataBlob = new Blob([dataStr], { type: 'application/json' })
        const url = URL.createObjectURL(dataBlob)
        const link = document.createElement('a')
        link.href = url
        link.download = `all-items-${new Date().toISOString().split('T')[0]}.json`
        link.click()
      } catch (error) {
        alert('Failed to export data')
      }
    },
    async exportAllCSV() {
      try {
        const response = await itemService.getAll()
        const items = response.data.results || response.data
        const headers = [
          'ID',
          'Title',
          'Description',
          'Category',
          'Priority',
          'Completed',
          'Due Date',
          'Tags',
          'Created At',
        ]
        const rows = items.map(item => [
          item.id,
          item.title,
          item.description || '',
          item.category || '',
          item.priority || '',
          item.completed ? 'Yes' : 'No',
          item.due_date || '',
          (item.tags_list || []).join('; '),
          item.created_at,
        ])
        const csvContent = [
          headers.join(','),
          ...rows.map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(',')),
        ].join('\n')
        const blob = new Blob([csvContent], { type: 'text/csv' })
        const url = URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `all-items-${new Date().toISOString().split('T')[0]}.csv`
        link.click()
      } catch (error) {
        alert('Failed to export data')
      }
    },
  },
}
</script>

<style scoped>
.page-header {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid var(--border-color);
}

.page-header h1 {
  color: var(--text-primary);
  font-size: 2rem;
}

.settings-content {
  max-width: 800px;
}

.settings-section {
  margin-bottom: 40px;
  background: var(--bg-secondary);
  padding: 25px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.settings-section h2 {
  color: var(--text-primary);
  font-size: 1.3rem;
  margin-bottom: 20px;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid var(--border-color);
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-info {
  flex: 1;
}

.setting-info label {
  display: block;
  color: var(--text-primary);
  font-weight: 600;
  margin-bottom: 5px;
}

.setting-description {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin: 0;
}

.setting-actions {
  display: flex;
  gap: 10px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.info-item {
  display: flex;
  flex-direction: column;
  padding: 15px;
  background: var(--bg-tertiary);
  border-radius: 6px;
}

.info-label {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-bottom: 5px;
}

.info-value {
  color: var(--text-primary);
  font-weight: 600;
  font-size: 1rem;
}
</style>
