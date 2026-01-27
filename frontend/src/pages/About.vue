<template>
  <div class="page-content">
    <div class="page-header">
      <h1>About This Application</h1>
    </div>

    <div class="about-content">
      <section class="about-section">
        <h2>📝 Todo Items Manager</h2>
        <p>
          This app is a complete task and item management system built with modern web technologies.
        </p>
      </section>

      <section class="about-section">
        <h2>✨ Features</h2>
        <ul class="features-list">
          <li>✅ Create, Read, Update, Delete (CRUD) operations</li>
          <li>🔍 Search and filter items</li>
          <li>📊 Dashboard with statistics and charts</li>
          <li>🏷️ Categories and priority levels</li>
          <li>📅 Due dates with calendar picker</li>
          <li>☑️ Bulk operations</li>
          <li>🌙 Dark mode support</li>
          <li>📤 Export to JSON and CSV</li>
          <li>📱 Responsive design</li>
        </ul>
      </section>

      <section class="about-section">
        <h2>🛠️ Technologies Used</h2>
        <div class="tech-grid">
          <div class="tech-card">
            <h3>Backend</h3>
            <ul>
              <li>Django 4.2.7</li>
              <li>Django REST Framework</li>
              <li>SQLite Database</li>
              <li>Custom Middleware</li>
            </ul>
          </div>
          <div class="tech-card">
            <h3>Frontend</h3>
            <ul>
              <li>Vue.js 3</li>
              <li>Vue Router</li>
              <li>Vite</li>
              <li>Axios</li>
            </ul>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'About',
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

.about-content {
  max-width: 900px;
}

.about-section {
  margin-bottom: 40px;
}

.about-section h2 {
  color: var(--text-primary);
  font-size: 1.5rem;
  margin-bottom: 15px;
}

.about-section p {
  color: var(--text-secondary);
  line-height: 1.8;
  font-size: 1rem;
}

.features-list {
  list-style: none;
  padding: 0;
}

.features-list li {
  padding: 10px 0;
  color: var(--text-secondary);
  font-size: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.features-list li:last-child {
  border-bottom: none;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.tech-card {
  background: var(--bg-secondary);
  padding: 20px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.tech-card h3 {
  color: var(--text-primary);
  margin-bottom: 15px;
  font-size: 1.2rem;
}

.tech-card ul {
  list-style: none;
  padding: 0;
}

.tech-card li {
  padding: 8px 0;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-color);
}

.tech-card li:last-child {
  border-bottom: none;
}

.api-endpoints {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 20px;
}

.endpoint {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 12px 15px;
  background: var(--bg-secondary);
  border-radius: 6px;
  border: 1px solid var(--border-color);
}

.endpoint code {
  background: var(--bg-tertiary);
  padding: 6px 12px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  color: var(--primary);
  font-weight: 600;
  min-width: 200px;
}

.endpoint span {
  color: var(--text-secondary);
}
</style>
