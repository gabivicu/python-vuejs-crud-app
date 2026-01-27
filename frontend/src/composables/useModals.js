export function useModals() {
  const showModal = { value: false }
  const showDeleteModal = { value: false }
  const editingItem = { value: null }
  const itemToDelete = { value: null }

  /**
   * Opens create modal
   */
  const openCreateModal = () => {
    editingItem.value = null
    showModal.value = true
  }

  /**
   * Opens edit modal with item data
   * @param {Object} item - Item to edit
   */
  const openEditModal = (item) => {
    editingItem.value = item
    showModal.value = true
  }

  /**
   * Closes create/edit modal
   */
  const closeModal = () => {
    showModal.value = false
    editingItem.value = null
  }

  /**
   * Opens delete confirmation modal
   * @param {Object} item - Item to delete
   */
  const openDeleteModal = (item) => {
    itemToDelete.value = item
    showDeleteModal.value = true
  }

  /**
   * Closes delete confirmation modal
   */
  const closeDeleteModal = () => {
    showDeleteModal.value = false
    itemToDelete.value = null
  }

  return {
    showModal,
    showDeleteModal,
    editingItem,
    itemToDelete,
    openCreateModal,
    openEditModal,
    closeModal,
    openDeleteModal,
    closeDeleteModal
  }
}
