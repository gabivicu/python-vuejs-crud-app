<template>
  <div :class="['modal', { active: isOpen }]" @click.self="handleClose">
    <div class="modal-content bulk-action-modal">
      <div class="modal-header">
        <h2>{{ title }}</h2>
        <button class="close-btn" @click="handleClose">&times;</button>
      </div>

      <div class="modal-body">
        <div class="warning-message">
          <p class="warning-text">{{ message }}</p>
          <p v-if="actionType === 'delete'" class="warning-subtext">
            This action cannot be undone.
          </p>
        </div>

        <div class="items-list-container">
          <h3 class="items-list-title">
            {{ items.length }} {{ items.length === 1 ? 'item' : 'items' }} to be
            {{ actionType === 'complete' ? 'marked as complete' : 'deleted' }}:
          </h3>
          <div class="items-preview-list">
            <div v-for="item in items" :key="item.id" class="item-preview-card">
              <div class="item-preview-header">
                <span class="item-id">#{{ item.id }}</span>
                <span :class="['badge', `badge-${item.priority || 'medium'}`]">
                  {{ getPriorityLabel(item.priority) }}
                </span>
                <span :class="['badge', item.completed ? 'badge-completed' : 'badge-pending']">
                  {{ item.completed ? 'Completed' : 'Pending' }}
                </span>
              </div>
              <div class="item-preview-title">{{ item.title }}</div>
              <div v-if="item.description" class="item-preview-description">
                {{ item.description }}
              </div>
              <div class="item-preview-meta">
                <span v-if="item.due_date" :class="['due-date', { overdue: isOverdue(item) }]">
                  Due: {{ formatDate(item.due_date) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="modal-actions">
        <button class="btn btn-secondary" @click="handleClose">Cancel</button>
        <button
          class="btn"
          :class="actionType === 'delete' ? 'btn-danger' : 'btn-success'"
          :disabled="isProcessing"
          @click="handleConfirm"
        >
          <span v-if="isProcessing">Processing...</span>
          <span v-else>{{ confirmButtonText }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { formatDate, isOverdue, getPriorityLabel } from '../utils/formatters'

export default {
  name: 'BulkActionModal',
  props: {
    isOpen: {
      type: Boolean,
      default: false,
    },
    actionType: {
      type: String,
      required: true,
      validator: value => ['complete', 'delete'].includes(value),
    },
    items: {
      type: Array,
      default: () => [],
    },
    isProcessing: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['close', 'confirm'],
  computed: {
    title() {
      return this.actionType === 'complete' ? 'Mark Items as Complete' : 'Delete Items'
    },
    message() {
      return this.actionType === 'complete'
        ? `Are you sure you want to mark ${this.items.length} ${this.items.length === 1 ? 'item' : 'items'} as complete?`
        : `Are you sure you want to delete ${this.items.length} ${this.items.length === 1 ? 'item' : 'items'}?`
    },
    confirmButtonText() {
      return this.actionType === 'complete' ? 'Mark Complete' : 'Delete Items'
    },
  },
  methods: {
    handleClose() {
      if (!this.isProcessing) {
        this.$emit('close')
      }
    },
    handleConfirm() {
      if (!this.isProcessing) {
        this.$emit('confirm')
      }
    },
    formatDate,
    isOverdue: item => isOverdue(item.due_date, item.completed),
    getPriorityLabel,
  },
}
</script>

<style scoped>
.bulk-action-modal {
  max-width: 700px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  width: 90%;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.warning-message {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #fff3cd;
  border-left: 4px solid #ffc107;
  border-radius: 4px;
}

.warning-text {
  margin: 0 0 8px 0;
  font-weight: 500;
  color: #856404;
}

.warning-subtext {
  margin: 0;
  font-size: 0.9rem;
  color: #856404;
}

.items-list-container {
  margin-top: 20px;
}

.items-list-title {
  margin: 0 0 15px 0;
  font-size: 1rem;
  font-weight: 600;
  color: #333;
}

.items-preview-list {
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 10px;
  background-color: #f9f9f9;
}

.item-preview-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 12px;
  margin-bottom: 10px;
  transition: box-shadow 0.2s;
}

.item-preview-card:last-child {
  margin-bottom: 0;
}

.item-preview-card:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.item-preview-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.item-id {
  font-weight: 600;
  color: #666;
  font-size: 0.85rem;
}

.item-preview-title {
  font-weight: 500;
  color: #333;
  margin-bottom: 6px;
  font-size: 0.95rem;
}

.item-preview-description {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 6px;
  line-height: 1.4;
}

.item-preview-meta {
  font-size: 0.8rem;
  color: #999;
}

.due-date.overdue {
  color: #dc3545;
  font-weight: 500;
}

.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.badge-medium {
  background-color: #ffc107;
  color: #856404;
}

.badge-high {
  background-color: #fd7e14;
  color: #fff;
}

.badge-low {
  background-color: #28a745;
  color: #fff;
}

.badge-urgent {
  background-color: #dc3545;
  color: #fff;
}

.badge-completed {
  background-color: #28a745;
  color: #fff;
}

.badge-pending {
  background-color: #ffc107;
  color: #856404;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 20px;
  border-top: 1px solid #e0e0e0;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #5a6268;
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background-color: #218838;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background-color: #c82333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #999;
  line-height: 1;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #333;
}
</style>
