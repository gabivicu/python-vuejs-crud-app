<template>
  <div class="min-h-screen">
    <!-- Header -->
    <header class="border-b-2 border-gray-200 bg-gradient-to-r from-white to-gray-50 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center gap-4">
            <h1
              class="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent"
            >
              Tasks
            </h1>
            <span class="text-sm font-semibold text-gray-600 bg-gray-100 px-3 py-1 rounded-full">
              {{ stats.total || 0 }} total
            </span>
          </div>
          <div class="flex items-center gap-3">
            <button
              class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border-2 border-gray-300 rounded-lg hover:border-gray-400 hover:bg-gray-50 transition-all shadow-sm hover:shadow"
              @click="toggleDashboard"
            >
              <BarChart3 :size="16" />
              Stats
            </button>
            <button
              class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg hover:from-blue-700 hover:to-blue-800 shadow-md hover:shadow-lg transition-all"
              @click="openCreateModal"
            >
              <Plus :size="16" />
              New Task
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Dashboard Stats (if visible) -->
    <div v-if="showDashboard" class="border-b bg-gradient-to-b from-gray-50 to-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-5">
          <div
            class="p-5 bg-gradient-to-br from-blue-50 to-blue-100 border-2 border-blue-200 rounded-xl shadow-sm hover:shadow-md transition-shadow"
          >
            <p class="text-sm font-medium text-blue-700 mb-1">Total</p>
            <p class="text-3xl font-bold text-blue-900">{{ stats.total || 0 }}</p>
          </div>
          <div
            class="p-5 bg-gradient-to-br from-emerald-50 to-emerald-100 border-2 border-emerald-200 rounded-xl shadow-sm hover:shadow-md transition-shadow"
          >
            <p class="text-sm font-medium text-emerald-700 mb-1">Completed</p>
            <p class="text-3xl font-bold text-emerald-900">{{ stats.completed || 0 }}</p>
          </div>
          <div
            class="p-5 bg-gradient-to-br from-amber-50 to-amber-100 border-2 border-amber-200 rounded-xl shadow-sm hover:shadow-md transition-shadow"
          >
            <p class="text-sm font-medium text-amber-700 mb-1">Pending</p>
            <p class="text-3xl font-bold text-amber-900">{{ stats.pending || 0 }}</p>
          </div>
          <div
            class="p-5 bg-gradient-to-br from-red-50 to-red-100 border-2 border-red-200 rounded-xl shadow-sm hover:shadow-md transition-shadow"
          >
            <p class="text-sm font-medium text-red-700 mb-1">Overdue</p>
            <p class="text-3xl font-bold text-red-900">{{ stats.overdue || 0 }}</p>
          </div>
          <div
            class="p-5 bg-gradient-to-br from-purple-50 to-purple-100 border-2 border-purple-200 rounded-xl shadow-sm hover:shadow-md transition-shadow"
          >
            <p class="text-sm font-medium text-purple-700 mb-1">Completion</p>
            <p class="text-3xl font-bold text-purple-900">{{ stats.completion_rate || 0 }}%</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Filters & Search -->
      <div class="mb-6 space-y-4">
        <div class="relative">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-blue-500" :size="18" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search tasks..."
            class="w-full pl-10 pr-4 py-3 text-sm bg-white border-2 border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all shadow-sm hover:shadow"
            @input="debouncedSearch"
          />
        </div>

        <div class="flex flex-wrap items-center gap-2">
          <select
            v-model="filters.category"
            class="px-3 py-2 text-sm bg-white border-2 border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all shadow-sm hover:shadow font-medium"
            @change="applyFilters"
          >
            <option value="">All Categories</option>
            <option value="work">Work</option>
            <option value="personal">Personal</option>
            <option value="shopping">Shopping</option>
            <option value="health">Health</option>
            <option value="finance">Finance</option>
            <option value="other">Other</option>
          </select>

          <select
            v-model="filters.priority"
            class="px-3 py-2 text-sm bg-white border-2 border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all shadow-sm hover:shadow font-medium"
            @change="applyFilters"
          >
            <option value="">All Priorities</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>

          <select
            v-model="filters.completed"
            class="px-3 py-2 text-sm bg-white border-2 border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all shadow-sm hover:shadow font-medium"
            @change="applyFilters"
          >
            <option value="">All Status</option>
            <option value="true">Completed</option>
            <option value="false">Pending</option>
          </select>

          <select
            v-model="sortBy"
            class="px-3 py-2 text-sm bg-white border-2 border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all shadow-sm hover:shadow font-medium"
            @change="applyFilters"
          >
            <option value="-created_at">Newest First</option>
            <option value="created_at">Oldest First</option>
            <option value="due_date">Due Date</option>
            <option value="-priority">Priority</option>
            <option value="title">Title A-Z</option>
          </select>

          <button
            v-if="hasActiveFilters"
            class="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-red-600 bg-red-50 border-2 border-red-200 rounded-lg hover:bg-red-100 hover:border-red-300 transition-all shadow-sm"
            @click="clearFilters"
          >
            <X :size="14" />
            Clear
          </button>
        </div>

        <!-- Bulk Actions -->
        <div
          v-if="selectedItems.length > 0"
          class="flex items-center gap-3 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border-2 border-blue-200 shadow-sm"
        >
          <span class="text-sm font-semibold text-blue-700"
            >{{ selectedItems.length }} selected</span
          >
          <button
            class="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-white bg-gradient-to-r from-emerald-500 to-emerald-600 rounded-md hover:from-emerald-600 hover:to-emerald-700 shadow-sm hover:shadow transition-all"
            @click="bulkComplete"
          >
            <CheckCheck :size="14" />
            Mark Complete
          </button>
          <button
            class="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-white bg-gradient-to-r from-red-500 to-red-600 rounded-md hover:from-red-600 hover:to-red-700 shadow-sm hover:shadow transition-all"
            @click="bulkDelete"
          >
            <Trash2 :size="14" />
            Delete
          </button>
          <button
            class="text-sm text-muted-foreground hover:text-foreground transition-colors"
            @click="clearSelection"
          >
            Clear
          </button>
        </div>
      </div>

      <!-- Messages -->
      <div
        v-if="error"
        class="mb-4 p-3 bg-destructive/10 text-destructive text-sm rounded-lg border border-destructive/20 flex items-start gap-2"
      >
        <AlertCircle :size="16" class="mt-0.5 flex-shrink-0" />
        <span>{{ error }}</span>
      </div>
      <div
        v-if="success"
        class="mb-4 p-3 bg-success/10 text-success text-sm rounded-lg border border-success/20 flex items-start gap-2"
      >
        <CheckCircle2 :size="16" class="mt-0.5 flex-shrink-0" />
        <span>{{ success }}</span>
      </div>

      <!-- Loading -->
      <div v-if="loading && items.length === 0" class="flex items-center justify-center py-16">
        <Loader2 class="animate-spin text-muted-foreground" :size="24" />
      </div>

      <!-- Empty State -->
      <div
        v-else-if="items.length === 0"
        class="flex flex-col items-center justify-center py-16 text-center"
      >
        <div
          class="w-20 h-20 mb-4 rounded-full bg-gradient-to-br from-blue-100 to-indigo-100 flex items-center justify-center shadow-lg"
        >
          <ListTodo :size="40" class="text-blue-600" />
        </div>
        <h3 class="text-xl font-bold text-gray-800 mb-2">No tasks found</h3>
        <p class="text-sm text-gray-600 mb-6">
          {{
            hasActiveFilters
              ? 'Try adjusting your filters'
              : 'Get started by creating your first task'
          }}
        </p>
        <button
          v-if="!hasActiveFilters"
          class="inline-flex items-center gap-2 px-6 py-3 text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg hover:from-blue-700 hover:to-blue-800 shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
          @click="openCreateModal"
        >
          <Plus :size="18" />
          Create Task
        </button>
      </div>

      <!-- Tasks List -->
      <div v-else class="space-y-2">
        <div
          v-for="item in items"
          :key="item.id"
          class="group p-4 bg-white border-2 rounded-lg hover:shadow-md transition-all"
          :class="{
            'ring-2 ring-blue-500 border-blue-300': selectedItems.includes(item.id),
            'border-red-300': isOverdue(item) && !item.completed,
            'border-gray-200':
              !selectedItems.includes(item.id) && (!isOverdue(item) || item.completed),
          }"
        >
          <div class="flex items-start gap-3">
            <input
              type="checkbox"
              :checked="selectedItems.includes(item.id)"
              class="mt-1 w-4 h-4 rounded border-muted-foreground/30 text-primary focus:ring-2 focus:ring-ring cursor-pointer"
              @change="toggleSelection(item.id)"
            />

            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-4">
                <div class="flex-1 min-w-0">
                  <h3
                    class="text-base font-semibold mb-1.5 text-gray-900"
                    :class="{ 'line-through text-gray-400': item.completed }"
                  >
                    {{ item.title }}
                  </h3>
                  <p
                    v-if="item.description"
                    class="text-sm text-gray-600 mb-3 line-clamp-2 leading-relaxed"
                  >
                    {{ item.description }}
                  </p>

                  <div class="flex flex-wrap items-center gap-2 text-xs">
                    <span
                      class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md font-medium text-white shadow-sm"
                      :class="getCategoryClass(item.category)"
                    >
                      {{ getCategoryLabel(item.category) }}
                    </span>
                    <span
                      class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md font-medium text-white shadow-sm"
                      :class="getPriorityClass(item.priority)"
                    >
                      {{ getPriorityLabel(item.priority) }}
                    </span>
                    <span
                      v-if="item.completed"
                      class="inline-flex items-center gap-1 px-2.5 py-1 rounded-md font-medium bg-emerald-500 text-white shadow-sm"
                    >
                      <CheckCircle2 :size="12" />
                      Completed
                    </span>
                    <span
                      v-if="item.due_date"
                      class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-xs font-medium"
                      :class="
                        isOverdue(item) && !item.completed
                          ? 'bg-red-100 text-red-700 border border-red-300'
                          : 'bg-gray-100 text-gray-700 border border-gray-300'
                      "
                    >
                      <Calendar :size="12" />
                      {{ formatDate(item.due_date) }}
                      <span v-if="isOverdue(item) && !item.completed" class="ml-1">⚠️</span>
                    </span>
                  </div>

                  <div
                    v-if="item.tags_list && item.tags_list.length > 0"
                    class="flex flex-wrap gap-1.5 mt-2"
                  >
                    <span
                      v-for="tag in item.tags_list"
                      :key="tag"
                      class="inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full bg-blue-50 text-blue-700 border border-blue-200 font-medium"
                    >
                      <Tag :size="10" />
                      {{ tag }}
                    </span>
                  </div>
                </div>

                <div
                  class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <button
                    class="p-2 text-muted-foreground hover:text-foreground hover:bg-accent rounded-md transition-colors"
                    :title="item.completed ? 'Mark as pending' : 'Mark as complete'"
                    @click="toggleComplete(item)"
                  >
                    <CheckCircle2 v-if="!item.completed" :size="16" />
                    <Circle v-else :size="16" />
                  </button>
                  <button
                    class="p-2 text-muted-foreground hover:text-foreground hover:bg-accent rounded-md transition-colors"
                    title="Edit"
                    @click="openEditModal(item)"
                  >
                    <Pencil :size="16" />
                  </button>
                  <button
                    class="p-2 text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded-md transition-colors"
                    title="Delete"
                    @click="deleteItem(item.id)"
                  >
                    <Trash2 :size="16" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Infinite Scroll Trigger -->
      <div ref="loadMoreTrigger" class="mt-6 flex items-center justify-center">
        <div
          v-if="loading && pagination.currentPage > 1"
          class="flex items-center gap-2 text-sm text-muted-foreground"
        >
          <Loader2 class="animate-spin" :size="16" />
          Loading more...
        </div>
        <div
          v-else-if="!pagination.hasNext && items.length > 0"
          class="text-sm text-muted-foreground"
        >
          No more tasks
        </div>
      </div>
    </main>

    <!-- Modal (simplified version - you can expand this) -->
    <div
      v-if="showModal"
      class="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm flex items-center justify-center p-4"
      @click.self="closeModal"
    >
      <div class="w-full max-w-lg bg-background border rounded-lg shadow-lg">
        <div class="flex items-center justify-between p-6 border-b">
          <h2 class="text-lg font-semibold">
            {{ editingItem ? 'Edit Task' : 'Create Task' }}
          </h2>
          <button
            class="p-1 text-muted-foreground hover:text-foreground rounded-md hover:bg-accent transition-colors"
            @click="closeModal"
          >
            <X :size="20" />
          </button>
        </div>

        <form class="p-6 space-y-4" @submit.prevent="saveItem">
          <div>
            <label class="text-sm font-medium mb-1.5 block">Title *</label>
            <input
              v-model="formData.title"
              type="text"
              required
              class="w-full px-3 py-2 text-sm bg-background border rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
              placeholder="Enter task title"
            />
          </div>

          <div>
            <label class="text-sm font-medium mb-1.5 block">Description</label>
            <textarea
              v-model="formData.description"
              rows="3"
              class="w-full px-3 py-2 text-sm bg-background border rounded-lg focus:outline-none focus:ring-2 focus:ring-ring resize-none"
              placeholder="Add more details..."
            ></textarea>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-sm font-medium mb-1.5 block">Category</label>
              <select
                v-model="formData.category"
                class="w-full px-3 py-2 text-sm bg-background border rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
              >
                <option value="work">Work</option>
                <option value="personal">Personal</option>
                <option value="shopping">Shopping</option>
                <option value="health">Health</option>
                <option value="finance">Finance</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div>
              <label class="text-sm font-medium mb-1.5 block">Priority</label>
              <select
                v-model="formData.priority"
                class="w-full px-3 py-2 text-sm bg-background border rounded-lg focus:outline-none focus:ring-2 focus:ring-ring"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>
          </div>

          <div class="flex items-center gap-2">
            <input
              id="completed"
              v-model="formData.completed"
              type="checkbox"
              class="w-4 h-4 rounded border-muted-foreground/30 text-primary focus:ring-2 focus:ring-ring"
            />
            <label for="completed" class="text-sm font-medium cursor-pointer"
              >Mark as completed</label
            >
          </div>

          <div class="flex justify-end gap-3 pt-4">
            <button
              type="button"
              class="px-4 py-2 text-sm font-medium text-foreground bg-background border rounded-lg hover:bg-accent transition-colors"
              @click="closeModal"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 text-sm font-medium text-primary-foreground bg-primary rounded-lg hover:opacity-90 transition-opacity"
            >
              {{ editingItem ? 'Update' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import {
  Plus,
  Search,
  X,
  CheckCheck,
  Trash2,
  AlertCircle,
  CheckCircle2,
  Loader2,
  ListTodo,
  Calendar,
  Tag,
  CheckCircle2 as Circle,
  Pencil,
  BarChart3,
} from 'lucide-vue-next'
import { itemService } from '../api'

// Props
const props = defineProps({
  showDashboard: {
    type: Boolean,
    default: false,
  },
  createModalTrigger: {
    type: Number,
    default: 0,
  },
})

// State
const items = ref([])
const loading = ref(false)
const error = ref(null)
const success = ref(null)
const showModal = ref(false)
const editingItem = ref(null)
const selectedItems = ref([])
const searchQuery = ref('')
const searchTimeout = ref(null)
const stats = ref({})
const showDashboard = ref(props.showDashboard)

// Watch for createModalTrigger prop changes
watch(
  () => props.createModalTrigger,
  newVal => {
    if (newVal > 0) {
      openCreateModal()
    }
  }
)

const pagination = ref({
  currentPage: 1,
  totalPages: 1,
  totalCount: 0,
  pageSize: 10,
  hasNext: false,
  hasPrevious: false,
})

const filters = ref({
  category: '',
  priority: '',
  completed: '',
  due_filter: '',
})

const sortBy = ref('-created_at')

const formData = ref({
  title: '',
  description: '',
  completed: false,
  category: 'other',
  priority: 'medium',
  due_date: '',
  tags: '',
})

const loadMoreTrigger = ref(null)
const observer = ref(null)

// Computed
const hasActiveFilters = computed(() => {
  return Object.values(filters.value).some(v => v !== '') || searchQuery.value !== ''
})

// Methods
const fetchItems = async () => {
  loading.value = true
  error.value = null
  try {
    const params = {
      ordering: sortBy.value,
    }

    let currentPage = pagination.value?.currentPage || 1
    if (currentPage > 1) {
      params.page = currentPage
    }

    if (filters.value.category) params.category = filters.value.category
    if (filters.value.priority) params.priority = filters.value.priority
    if (filters.value.completed) params.completed = filters.value.completed
    if (filters.value.due_filter) params.due_filter = filters.value.due_filter
    if (searchQuery.value) params.search = searchQuery.value

    const response = await itemService.getAll(params)

    if (response.data && typeof response.data === 'object') {
      if (Array.isArray(response.data.results)) {
        if (currentPage === 1) {
          items.value = response.data.results
        } else {
          const newItems = response.data.results.filter(
            newItem => !items.value.some(existingItem => existingItem.id === newItem.id)
          )
          items.value = [...items.value, ...newItems]
        }

        const pageSize = 10
        const count = response.data.count || 0
        const nextUrl = response.data.next
        const previousUrl = response.data.previous

        pagination.value = {
          currentPage: currentPage,
          totalPages: Math.ceil(count / pageSize),
          totalCount: count,
          pageSize: pageSize,
          hasNext: !!nextUrl,
          hasPrevious: !!previousUrl,
        }
      } else if (Array.isArray(response.data)) {
        items.value = response.data
      }
    }
  } catch (err) {
    error.value = 'Failed to load tasks. Please try again.'
    console.error('Error fetching items:', err)
  } finally {
    loading.value = false
  }
}

const fetchStats = async () => {
  try {
    const response = await itemService.getStats()
    stats.value = response.data
  } catch (err) {
    console.error('Error fetching stats:', err)
  }
}

const debouncedSearch = () => {
  clearTimeout(searchTimeout.value)
  searchTimeout.value = setTimeout(() => {
    applyFilters()
  }, 300)
}

const applyFilters = () => {
  pagination.value.currentPage = 1
  fetchItems()
  fetchStats()
}

const clearFilters = () => {
  filters.value = {
    category: '',
    priority: '',
    completed: '',
    due_filter: '',
  }
  searchQuery.value = ''
  sortBy.value = '-created_at'
  pagination.value.currentPage = 1
  applyFilters()
}

const toggleSelection = itemId => {
  const index = selectedItems.value.indexOf(itemId)
  if (index > -1) {
    selectedItems.value.splice(index, 1)
  } else {
    selectedItems.value.push(itemId)
  }
}

const clearSelection = () => {
  selectedItems.value = []
}

const bulkComplete = async () => {
  if (selectedItems.value.length === 0) return
  try {
    await itemService.bulkUpdate(selectedItems.value, { completed: true })
    success.value = `${selectedItems.value.length} tasks marked as complete`
    clearSelection()
    await fetchItems()
    await fetchStats()
    setTimeout(() => {
      success.value = null
    }, 3000)
  } catch (err) {
    error.value = 'Failed to update tasks'
  }
}

const bulkDelete = async () => {
  if (selectedItems.value.length === 0) return
  if (!confirm(`Delete ${selectedItems.value.length} tasks?`)) return

  try {
    await itemService.bulkDelete(selectedItems.value)
    success.value = `${selectedItems.value.length} tasks deleted`
    clearSelection()
    await fetchItems()
    await fetchStats()
    setTimeout(() => {
      success.value = null
    }, 3000)
  } catch (err) {
    error.value = 'Failed to delete tasks'
  }
}

const openCreateModal = () => {
  editingItem.value = null
  formData.value = {
    title: '',
    description: '',
    completed: false,
    category: 'other',
    priority: 'medium',
    due_date: '',
    tags: '',
  }
  showModal.value = true
  error.value = null
  success.value = null
}

const openEditModal = item => {
  editingItem.value = item
  formData.value = {
    title: item.title,
    description: item.description || '',
    completed: item.completed,
    category: item.category || 'other',
    priority: item.priority || 'medium',
    due_date: item.due_date || '',
    tags: item.tags || '',
  }
  showModal.value = true
  error.value = null
  success.value = null
}

const closeModal = () => {
  showModal.value = false
  editingItem.value = null
}

const saveItem = async () => {
  error.value = null
  success.value = null
  try {
    const data = { ...formData.value }

    if (editingItem.value) {
      await itemService.update(editingItem.value.id, data)
      success.value = 'Task updated successfully'
    } else {
      await itemService.create(data)
      success.value = 'Task created successfully'
    }

    closeModal()
    await fetchItems()
    await fetchStats()
    setTimeout(() => {
      success.value = null
    }, 3000)
  } catch (err) {
    error.value = 'Failed to save task'
    console.error('Error saving item:', err)
  }
}

const deleteItem = async id => {
  if (!confirm('Delete this task?')) return

  try {
    await itemService.delete(id)
    success.value = 'Task deleted successfully'
    await fetchItems()
    await fetchStats()
    setTimeout(() => {
      success.value = null
    }, 3000)
  } catch (err) {
    error.value = 'Failed to delete task'
    console.error('Error deleting item:', err)
  }
}

const toggleComplete = async item => {
  try {
    await itemService.patch(item.id, { completed: !item.completed })
    await fetchItems()
    await fetchStats()
  } catch (err) {
    error.value = 'Failed to update task'
  }
}

const formatDate = dateString => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

const getCategoryLabel = category => {
  const labels = {
    work: 'Work',
    personal: 'Personal',
    shopping: 'Shopping',
    health: 'Health',
    finance: 'Finance',
    other: 'Other',
  }
  return labels[category] || 'Other'
}

const getPriorityLabel = priority => {
  const labels = {
    low: 'Low',
    medium: 'Medium',
    high: 'High',
    urgent: 'Urgent',
  }
  return labels[priority] || 'Medium'
}

const isOverdue = item => {
  if (!item.due_date || item.completed) return false
  return new Date(item.due_date) < new Date()
}

const getCategoryClass = category => {
  const classes = {
    work: 'bg-blue-500 hover:bg-blue-600',
    personal: 'bg-purple-500 hover:bg-purple-600',
    shopping: 'bg-amber-500 hover:bg-amber-600',
    health: 'bg-emerald-500 hover:bg-emerald-600',
    finance: 'bg-red-500 hover:bg-red-600',
    other: 'bg-gray-500 hover:bg-gray-600',
  }
  return classes[category] || classes.other
}

const getPriorityClass = priority => {
  const classes = {
    low: 'bg-emerald-500 hover:bg-emerald-600',
    medium: 'bg-amber-500 hover:bg-amber-600',
    high: 'bg-orange-500 hover:bg-orange-600',
    urgent: 'bg-red-600 hover:bg-red-700',
  }
  return classes[priority] || classes.medium
}

const toggleDashboard = () => {
  showDashboard.value = !showDashboard.value
}

const setupIntersectionObserver = () => {
  const options = {
    root: null,
    rootMargin: '100px',
    threshold: 0.1,
  }

  observer.value = new IntersectionObserver(entries => {
    const entry = entries[0]
    if (entry && entry.isIntersecting) {
      loadMore()
    }
  }, options)

  if (loadMoreTrigger.value) {
    observer.value.observe(loadMoreTrigger.value)
  }
}

const loadMore = () => {
  if (loading.value || !pagination.value.hasNext) return
  pagination.value.currentPage++
  fetchItems()
}

// Lifecycle
onMounted(() => {
  fetchItems()
  fetchStats()
  setupIntersectionObserver()
})

onBeforeUnmount(() => {
  if (observer.value) {
    observer.value.disconnect()
  }
})
</script>
