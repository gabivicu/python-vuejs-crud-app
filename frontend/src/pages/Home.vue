<template>
  <div class="page-content">
    <!-- Header Actions (moved from App.vue) -->
    <div class="header-actions-mobile" v-if="false" style="display: none;">
      <!-- Hidden, actions are in App.vue header -->
    </div>
    <!-- Dashboard -->
    <div v-if="showDashboardProp" class="dashboard">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">{{ stats.total || 0 }}</div>
          <div class="stat-label">Total Items</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ stats.completed || 0 }}</div>
          <div class="stat-label">Completed</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ stats.pending || 0 }}</div>
          <div class="stat-label">Pending</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ stats.overdue || 0 }}</div>
          <div class="stat-label">Overdue</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ stats.completion_rate || 0 }}%</div>
          <div class="stat-label">Completion Rate</div>
        </div>
      </div>
      <div class="chart-container">
        <div class="chart-section">
          <h3>By Priority</h3>
          <div class="chart-bars">
            <div v-for="(count, priority) in stats.priority_stats" :key="priority" class="chart-bar">
              <div class="bar-label">{{ priority }}</div>
              <div class="bar-container">
                <div 
                  :class="['bar', `priority-${priority}`]"
                  :style="{ width: `${(count / (stats.total || 1)) * 100}%` }"
                ></div>
                <span class="bar-value">{{ count }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="chart-section">
          <h3>By Category</h3>
          <div class="chart-bars">
            <div v-for="(count, category) in stats.category_stats" :key="category" class="chart-bar">
              <div class="bar-label">{{ category }}</div>
              <div class="bar-container">
                <div 
                  class="bar category-bar"
                  :style="{ width: `${(count / (stats.total || 1)) * 100}%` }"
                ></div>
                <span class="bar-value">{{ count }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="filters-section">
      <div class="search-bar">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="🔍 Search items..."
          class="search-input"
          @input="debouncedSearch"
        />
      </div>
      <div class="filters-row">
        <select v-model="filters.category" @change="applyFilters" class="filter-select">
          <option value="">All Categories</option>
          <option value="work">Work</option>
          <option value="personal">Personal</option>
          <option value="shopping">Shopping</option>
          <option value="health">Health</option>
          <option value="finance">Finance</option>
          <option value="other">Other</option>
        </select>
        <select v-model="filters.priority" @change="applyFilters" class="filter-select">
          <option value="">All Priorities</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="urgent">Urgent</option>
        </select>
        <select v-model="filters.completed" @change="applyFilters" class="filter-select">
          <option value="">All Status</option>
          <option value="true">Completed</option>
          <option value="false">Pending</option>
        </select>
        <select v-model="filters.due_filter" @change="applyFilters" class="filter-select">
          <option value="">All Dates</option>
          <option value="overdue">Overdue</option>
          <option value="today">Today</option>
          <option value="upcoming">Upcoming</option>
        </select>
        <select v-model="sortBy" @change="applyFilters" class="filter-select">
          <option value="-created_at">Newest First</option>
          <option value="created_at">Oldest First</option>
          <option value="due_date">Due Date</option>
          <option value="-priority">Priority</option>
          <option value="title">Title A-Z</option>
        </select>
        <button @click="clearFilters" class="btn btn-secondary btn-small">Clear Filters</button>
      </div>
      <div class="bulk-actions" v-if="selectedItems.length > 0">
        <span class="selected-count">{{ selectedItems.length }} selected</span>
        <button @click="bulkComplete" class="btn btn-success btn-small">Mark Complete</button>
        <button @click="bulkDelete" class="btn btn-danger btn-small">Delete Selected</button>
        <button @click="clearSelection" class="btn btn-secondary btn-small">Clear Selection</button>
      </div>
      <div class="export-actions">
        <button @click="exportJSON" class="btn btn-secondary btn-small">Export JSON</button>
        <button @click="exportCSV" class="btn btn-secondary btn-small">Export CSV</button>
      </div>
    </div>

    <!-- Messages -->
    <div v-if="error" class="error">
      {{ error }}
    </div>
    <div v-if="success" class="success">
      {{ success }}
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      Loading items...
    </div>

    <!-- Empty State -->
    <div v-else-if="items.length === 0" class="empty-state">
      <h3>No items found</h3>
      <p v-if="hasActiveFilters">Try adjusting your filters</p>
      <p v-else>Click "Add New Item" to create your first item!</p>
    </div>

    <!-- Items List -->
    <div v-else class="items-list">
      <div 
        v-for="item in items" 
        :key="item.id" 
        :class="['item-card', { 'selected': selectedItems.includes(item.id), 'overdue': isOverdue(item) }]"
      >
        <div class="item-checkbox">
          <input 
            type="checkbox" 
            :checked="selectedItems.includes(item.id)"
            @change="toggleSelection(item.id)"
          />
        </div>
        <div class="item-content-wrapper">
          <div class="item-content">
            <div class="item-header">
              <h3 class="item-title">{{ item.title }}</h3>
              <div class="item-badges">
                <span :class="['badge', `badge-category-${item.category || 'other'}`]" title="Category">
                  {{ getCategoryLabel(item.category) }}
                </span>
                <span :class="['badge', `badge-${item.priority || 'medium'}`]" title="Priority">
                  {{ getPriorityLabel(item.priority) }}
                </span>
                <span :class="['badge', item.completed ? 'badge-completed' : 'badge-pending']" title="Status">
                  {{ item.completed ? 'Completed' : 'Pending' }}
                </span>
              </div>
            </div>
            <p v-if="item.description" class="item-description">{{ item.description }}</p>
            <div class="item-tags" v-if="item.tags_list && item.tags_list.length > 0">
              <span v-for="tag in item.tags_list" :key="tag" class="tag">{{ tag }}</span>
            </div>
            <div class="item-meta">
              <span>Created: {{ formatDate(item.created_at) }}</span>
              <span v-if="item.due_date" :class="['due-date', { 'overdue': isOverdue(item) }]">
                Due: {{ formatDate(item.due_date) }}
              </span>
            </div>
          </div>
          <div class="item-actions">
            <button @click="toggleComplete(item)" class="btn btn-small btn-success">
              {{ item.completed ? 'Mark Pending' : 'Mark Complete' }}
            </button>
            <button @click="openEditModal(item)" class="btn btn-small btn-secondary">
              Edit
            </button>
            <button @click="deleteItem(item.id)" class="btn btn-small btn-danger">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div :class="['modal', { active: showModal }]" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ editingItem ? 'Edit Item' : 'Create New Item' }}</h2>
          <button @click="closeModal" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="saveItem">
          <div class="form-group">
            <label for="title">Title *</label>
            <input
              id="title"
              v-model="formData.title"
              type="text"
              required
              placeholder="Enter item title"
            />
          </div>
          <div class="form-group">
            <label for="description">Description</label>
            <textarea
              id="description"
              v-model="formData.description"
              placeholder="Enter item description"
            ></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="category">Category</label>
              <select id="category" v-model="formData.category">
                <option value="work">Work</option>
                <option value="personal">Personal</option>
                <option value="shopping">Shopping</option>
                <option value="health">Health</option>
                <option value="finance">Finance</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div class="form-group">
              <label for="priority">Priority</label>
              <select id="priority" v-model="formData.priority">
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>Due Date</label>
            <div class="date-picker-wrapper">
              <div class="date-input" @click="showCalendar = !showCalendar">
                <span v-if="formData.due_date" class="selected-date-text">
                  {{ formatDisplayDate(formData.due_date) }}
                </span>
                <span v-else class="placeholder-date">Select a date...</span>
                <span class="calendar-icon">📅</span>
              </div>
              <button 
                v-if="formData.due_date" 
                type="button" 
                @click.stop="clearDueDate" 
                class="btn-clear-date-small"
              >
                ✕
              </button>
              <div v-if="showCalendar" class="calendar-popup" @click.stop>
                <div class="calendar-header">
                  <button @click.stop="previousMonth" type="button" class="calendar-nav-btn">‹</button>
                  <div class="calendar-month-year">
                    <span class="month-selector" @click.stop="showMonthSelector = !showMonthSelector">
                      {{ currentMonthName }}
                    </span>
                    <span class="year-selector" @click.stop="showYearSelector = !showYearSelector">
                      {{ currentYear }}
                    </span>
                  </div>
                  <button @click.stop="nextMonth" type="button" class="calendar-nav-btn">›</button>
                </div>
                <!-- Year Selector -->
                <div v-if="showYearSelector" class="year-selector-popup" @click.stop>
                  <div class="year-selector-header">
                    <button @click.stop="previousYearRange" type="button" class="year-nav-btn">‹‹</button>
                    <span class="year-range">{{ yearRangeStart }} - {{ yearRangeEnd }}</span>
                    <button @click.stop="nextYearRange" type="button" class="year-nav-btn">››</button>
                  </div>
                  <div class="year-grid">
                    <div
                      v-for="year in availableYearsList"
                      :key="year"
                      :class="['year-item', { 'selected': year === currentYear, 'current': year === new Date().getFullYear() }]"
                      @click.stop="selectYear(year)"
                    >
                      {{ year }}
                    </div>
                  </div>
                </div>
                <!-- Month Selector -->
                <div v-if="showMonthSelector" class="month-selector-popup" @click.stop>
                  <div class="month-grid">
                    <div
                      v-for="(month, index) in months"
                      :key="index"
                      :class="['month-item', { 'selected': index === currentMonth }]"
                      @click.stop="selectMonth(index)"
                    >
                      {{ month }}
                    </div>
                  </div>
                </div>
                <div class="calendar-weekdays">
                  <div v-for="day in weekDays" :key="day" class="weekday">{{ day }}</div>
                </div>
                <div class="calendar-days">
                  <div 
                    v-for="day in calendarDays" 
                    :key="day.key"
                    :class="['calendar-day', {
                      'other-month': day.otherMonth,
                      'today': day.isToday,
                      'selected': day.isSelected,
                      'disabled': day.isDisabled
                    }]"
                    @click.stop="selectDate(day)"
                  >
                    {{ day.day }}
                  </div>
                </div>
                <div class="calendar-actions">
                  <button @click.stop="clearDueDate" type="button" class="btn-calendar-cancel">Cancel</button>
                  <button @click.stop="applyDate" type="button" class="btn-calendar-apply">Apply</button>
                </div>
              </div>
            </div>
          </div>
          <div class="form-group">
            <label for="tags">Tags (comma-separated)</label>
            <input
              id="tags"
              v-model="formData.tags"
              type="text"
              placeholder="e.g., urgent, important, project"
            />
          </div>
          <div class="form-group">
            <div class="checkbox-group">
              <input
                id="completed"
                v-model="formData.completed"
                type="checkbox"
              />
              <label for="completed">Completed</label>
            </div>
          </div>
          <div class="form-actions">
            <button type="button" @click="closeModal" class="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary">
              {{ editingItem ? 'Update' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { itemService } from '../api'

export default {
  name: 'Home',
  props: {
    showDashboard: {
      type: Boolean,
      default: false,
    },
    createModalTrigger: {
      type: Number,
      default: 0
    }
  },
  watch: {
    createModalTrigger(newVal) {
      if (newVal > 0) {
        this.openCreateModal()
      }
    }
  },
  computed: {
    showDashboardProp() {
      return this.showDashboard
    },
  },
  data() {
    return {
      items: [],
      loading: false,
      error: null,
      success: null,
      showModal: false,
      editingItem: null,
      selectedItems: [],
      searchQuery: '',
      searchTimeout: null,
      stats: {},
      filters: {
        category: '',
        priority: '',
        completed: '',
        due_filter: '',
      },
      sortBy: '-created_at',
      formData: {
        title: '',
        description: '',
        completed: false,
        category: 'other',
        priority: 'medium',
        due_date: '',
        tags: '',
      },
      showCalendar: false,
      currentMonth: new Date().getMonth(),
      currentYear: new Date().getFullYear(),
      tempSelectedDate: null,
      showYearSelector: false,
      showMonthSelector: false,
      yearRangeStart: new Date().getFullYear() - 5,
      yearRangeEnd: new Date().getFullYear() + 6,
      weekDays: ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'],
      months: [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
      ],
    }
  },
  computed: {
    hasActiveFilters() {
      return Object.values(this.filters).some(v => v !== '') || this.searchQuery !== ''
    },
    currentMonthName() {
      return this.months[this.currentMonth]
    },
    availableYearsList() {
      const years = []
      for (let year = this.yearRangeStart; year <= this.yearRangeEnd; year++) {
        years.push(year)
      }
      return years
    },
    calendarDays() {
      const days = []
      const firstDay = new Date(this.currentYear, this.currentMonth, 1)
      const lastDay = new Date(this.currentYear, this.currentMonth + 1, 0)
      const daysInMonth = lastDay.getDate()
      const startingDayOfWeek = (firstDay.getDay() + 6) % 7 // Monday = 0
      
      const today = new Date()
      const todayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`
      
      // Previous month days
      const prevMonth = new Date(this.currentYear, this.currentMonth, 0)
      const prevMonthDays = prevMonth.getDate()
      for (let i = startingDayOfWeek - 1; i >= 0; i--) {
        const day = prevMonthDays - i
        const dateStr = `${prevMonth.getFullYear()}-${String(prevMonth.getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
        days.push({
          day: day,
          date: dateStr,
          otherMonth: true,
          isToday: false,
          isSelected: false,
          isDisabled: true,
          key: `prev-${day}`
        })
      }
      
      // Current month days
      const todayDate = new Date()
      todayDate.setHours(0, 0, 0, 0)
      
      for (let day = 1; day <= daysInMonth; day++) {
        const dateStr = `${this.currentYear}-${String(this.currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
        const date = new Date(this.currentYear, this.currentMonth, day)
        date.setHours(0, 0, 0, 0)
        const isToday = dateStr === todayStr
        
        const isSelected = this.tempSelectedDate === dateStr || (!this.tempSelectedDate && this.formData.due_date === dateStr)
        const isDisabled = false
        
        days.push({
          day: day,
          date: dateStr,
          otherMonth: false,
          isToday: isToday,
          isSelected: isSelected,
          isDisabled: isDisabled,
          key: `curr-${day}`
        })
      }
      
      // Next month days (to fill the grid)
      const remainingDays = 42 - days.length // 6 weeks * 7 days
      for (let day = 1; day <= remainingDays; day++) {
        const dateStr = `${this.currentYear}-${String(this.currentMonth + 2).padStart(2, '0')}-${String(day).padStart(2, '0')}`
        days.push({
          day: day,
          date: dateStr,
          otherMonth: true,
          isToday: false,
          isSelected: false,
          isDisabled: true,
          key: `next-${day}`
        })
      }
      
      return days
    },
  },
  mounted() {
    this.fetchItems()
    this.fetchStats()
    document.addEventListener('click', this.handleClickOutside)
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside)
  },
  methods: {
    async fetchItems() {
      this.loading = true
      this.error = null
      try {
        const params = {
          ordering: this.sortBy,
        }
        if (this.filters.category) params.category = this.filters.category
        if (this.filters.priority) params.priority = this.filters.priority
        if (this.filters.completed) params.completed = this.filters.completed
        if (this.filters.due_filter) params.due_filter = this.filters.due_filter
        if (this.searchQuery) params.search = this.searchQuery

        const response = await itemService.getAll(params)
        this.items = response.data.results || response.data
      } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message || 'Unknown error'
        this.error = `Failed to fetch items: ${errorMessage}. Make sure the Django server is running on port 8000.`
        console.error('Error fetching items:', {
          message: error.message,
          code: error.code,
          response: error.response?.data,
          config: error.config,
        })
      } finally {
        this.loading = false
      }
    },
    async fetchStats() {
      try {
        const response = await itemService.getStats()
        this.stats = response.data
      } catch (error) {
        console.error('Error fetching stats:', error)
      }
    },
    debouncedSearch() {
      clearTimeout(this.searchTimeout)
      this.searchTimeout = setTimeout(() => {
        this.applyFilters()
      }, 300)
    },
    applyFilters() {
      this.fetchItems()
      this.fetchStats()
    },
    clearFilters() {
      this.filters = {
        category: '',
        priority: '',
        completed: '',
        due_filter: '',
      }
      this.searchQuery = ''
      this.sortBy = '-created_at'
      this.applyFilters()
    },
    toggleSelection(itemId) {
      const index = this.selectedItems.indexOf(itemId)
      if (index > -1) {
        this.selectedItems.splice(index, 1)
      } else {
        this.selectedItems.push(itemId)
      }
    },
    clearSelection() {
      this.selectedItems = []
    },
    async bulkComplete() {
      if (!confirm(`Mark ${this.selectedItems.length} items as complete?`)) return
      try {
        await itemService.bulkUpdate(this.selectedItems, { completed: true })
        this.success = `${this.selectedItems.length} items marked as complete!`
        this.clearSelection()
        await this.fetchItems()
        await this.fetchStats()
        setTimeout(() => { this.success = null }, 3000)
      } catch (error) {
        this.error = 'Failed to update items'
      }
    },
    async bulkDelete() {
      if (!confirm(`Delete ${this.selectedItems.length} items?`)) return
      try {
        await itemService.bulkDelete(this.selectedItems)
        this.success = `${this.selectedItems.length} items deleted!`
        this.clearSelection()
        await this.fetchItems()
        await this.fetchStats()
        setTimeout(() => { this.success = null }, 3000)
      } catch (error) {
        this.error = 'Failed to delete items'
      }
    },
    openCreateModal() {
      this.editingItem = null
      this.formData = {
        title: '',
        description: '',
        completed: false,
        category: 'other',
        priority: 'medium',
        due_date: '',
        tags: '',
      }
      this.showCalendar = false
      this.tempSelectedDate = null
      this.currentMonth = new Date().getMonth()
      this.currentYear = new Date().getFullYear()
      this.showModal = true
      this.error = null
      this.success = null
    },
    openEditModal(item) {
      this.editingItem = item
      let formattedDueDate = ''
      if (item.due_date) {
        const date = new Date(item.due_date)
        const year = date.getFullYear()
        const month = String(date.getMonth() + 1).padStart(2, '0')
        const day = String(date.getDate()).padStart(2, '0')
        formattedDueDate = `${year}-${month}-${day}`
        this.currentMonth = date.getMonth()
        this.currentYear = date.getFullYear()
      } else {
        this.currentMonth = new Date().getMonth()
        this.currentYear = new Date().getFullYear()
      }
      this.formData = {
        title: item.title,
        description: item.description || '',
        completed: item.completed,
        category: item.category || 'other',
        priority: item.priority || 'medium',
        due_date: formattedDueDate,
        tags: item.tags || '',
      }
      this.showCalendar = false
      this.tempSelectedDate = null
      this.showModal = true
      this.error = null
      this.success = null
    },
    closeModal(event) {
      if (event && event.target.closest('.calendar-popup')) {
        return
      }
      this.showModal = false
      this.editingItem = null
      this.showCalendar = false
      this.showYearSelector = false
      this.showMonthSelector = false
      this.tempSelectedDate = null
      this.formData = {
        title: '',
        description: '',
        completed: false,
        category: 'other',
        priority: 'medium',
        due_date: '',
        tags: '',
      }
    },
    clearDueDate() {
      this.formData.due_date = ''
      this.tempSelectedDate = null
    },
    previousMonth() {
      if (this.currentMonth === 0) {
        this.currentMonth = 11
        this.currentYear--
      } else {
        this.currentMonth--
      }
      this.showYearSelector = false
      this.showMonthSelector = false
    },
    nextMonth() {
      if (this.currentMonth === 11) {
        this.currentMonth = 0
        this.currentYear++
      } else {
        this.currentMonth++
      }
      this.showYearSelector = false
      this.showMonthSelector = false
    },
    selectYear(year) {
      this.currentYear = year
      this.showYearSelector = false
      if (year < this.yearRangeStart) {
        const diff = this.yearRangeStart - year
        this.yearRangeStart = year
        this.yearRangeEnd -= diff
      } else if (year > this.yearRangeEnd) {
        const diff = year - this.yearRangeEnd
        this.yearRangeEnd = year
        this.yearRangeStart += diff
      }
    },
    selectMonth(monthIndex) {
      this.currentMonth = monthIndex
      this.showMonthSelector = false
    },
    previousYearRange() {
      const range = this.yearRangeEnd - this.yearRangeStart + 1
      this.yearRangeStart -= range
      this.yearRangeEnd -= range
    },
    nextYearRange() {
      const range = this.yearRangeEnd - this.yearRangeStart + 1
      this.yearRangeStart += range
      this.yearRangeEnd += range
    },
    selectDate(day) {
      if (day.isDisabled || day.otherMonth) return
      this.tempSelectedDate = day.date
    },
    applyDate() {
      if (this.tempSelectedDate) {
        this.formData.due_date = this.tempSelectedDate
      }
      this.showCalendar = false
    },
    async saveItem() {
      this.error = null
      this.success = null
      try {
        const data = { ...this.formData }
        if (data.due_date) {
          const dateStr = data.due_date + 'T23:59:59'
          data.due_date = new Date(dateStr).toISOString()
        } else {
          data.due_date = null
        }
        
        if (this.editingItem) {
          await itemService.update(this.editingItem.id, data)
          this.success = 'Item updated successfully!'
        } else {
          await itemService.create(data)
          this.success = 'Item created successfully!'
        }
        this.closeModal()
        await this.fetchItems()
        await this.fetchStats()
        setTimeout(() => {
          this.success = null
        }, 3000)
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to save item'
        console.error('Error saving item:', error)
      }
    },
    async deleteItem(id) {
      if (!confirm('Are you sure you want to delete this item?')) {
        return
      }
      this.error = null
      try {
        await itemService.delete(id)
        this.success = 'Item deleted successfully!'
        await this.fetchItems()
        await this.fetchStats()
        setTimeout(() => {
          this.success = null
        }, 3000)
      } catch (error) {
        this.error = 'Failed to delete item'
        console.error('Error deleting item:', error)
      }
    },
    async toggleComplete(item) {
      this.error = null
      try {
        await itemService.update(item.id, {
          ...item,
          completed: !item.completed,
        })
        await this.fetchItems()
        await this.fetchStats()
      } catch (error) {
        this.error = 'Failed to update item'
        console.error('Error updating item:', error)
      }
    },
    isOverdue(item) {
      if (!item.due_date || item.completed) return false
      return new Date(item.due_date) < new Date()
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })
    },
    formatDisplayDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      const day = date.getDate()
      const month = this.months[date.getMonth()]
      const year = date.getFullYear()
      return `${day} ${month} ${year}`
    },
    getPriorityLabel(priority) {
      const labels = {
        low: 'Low',
        medium: 'Medium',
        high: 'High',
        urgent: 'Urgent',
      }
      return labels[priority] || 'Medium'
    },
    getCategoryLabel(category) {
      const labels = {
        work: 'Work',
        personal: 'Personal',
        shopping: 'Shopping',
        health: 'Health',
        finance: 'Finance',
        other: 'Other',
      }
      return labels[category] || 'Other'
    },
    exportJSON() {
      const dataStr = JSON.stringify(this.items, null, 2)
      const dataBlob = new Blob([dataStr], { type: 'application/json' })
      const url = URL.createObjectURL(dataBlob)
      const link = document.createElement('a')
      link.href = url
      link.download = `items-${new Date().toISOString().split('T')[0]}.json`
      link.click()
    },
    exportCSV() {
      const headers = ['ID', 'Title', 'Description', 'Category', 'Priority', 'Completed', 'Due Date', 'Tags', 'Created At']
      const rows = this.items.map(item => [
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
        ...rows.map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(','))
      ].join('\n')
      const blob = new Blob([csvContent], { type: 'text/csv' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `items-${new Date().toISOString().split('T')[0]}.csv`
      link.click()
    },
    handleClickOutside(event) {
      const calendarPopup = event.target.closest('.calendar-popup')
      const dateInput = event.target.closest('.date-input')
      if (!calendarPopup && !dateInput && this.showCalendar) {
        this.showCalendar = false
        this.showYearSelector = false
        this.showMonthSelector = false
        if (this.tempSelectedDate) {
          this.formData.due_date = this.tempSelectedDate
          this.tempSelectedDate = null
        }
      }
    },
  },
}
</script>

<style scoped>
.page-content {
  width: 100%;
}
</style>

