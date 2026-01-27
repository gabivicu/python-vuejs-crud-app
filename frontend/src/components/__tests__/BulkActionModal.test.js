import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BulkActionModal from '../BulkActionModal.vue'

describe('BulkActionModal', () => {
  const mockItems = [
    {
      id: 1,
      title: 'Test Item 1',
      description: 'Description 1',
      priority: 'high',
      completed: false,
      due_date: '2024-12-31T00:00:00Z',
    },
    {
      id: 2,
      title: 'Test Item 2',
      description: 'Description 2',
      priority: 'medium',
      completed: true,
      due_date: null,
    },
  ]

  describe('rendering', () => {
    it('should render when isOpen is true', () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'complete',
          items: mockItems,
        },
      })

      expect(wrapper.find('.modal').classes()).toContain('active')
      expect(wrapper.find('.modal-content').exists()).toBe(true)
    })

    it('should not render when isOpen is false', () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: false,
          actionType: 'complete',
          items: mockItems,
        },
      })

      expect(wrapper.find('.modal').classes()).not.toContain('active')
    })

    it('should display correct title for complete action', () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'complete',
          items: mockItems,
        },
      })

      expect(wrapper.find('h2').text()).toBe('Mark Items as Complete')
    })

    it('should display correct title for delete action', () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'delete',
          items: mockItems,
        },
      })

      expect(wrapper.find('h2').text()).toBe('Delete Items')
    })

    it('should display correct message for complete action', () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'complete',
          items: mockItems,
        },
      })

      const message = wrapper.find('.warning-text').text()
      expect(message).toContain('mark')
      expect(message).toContain('items')
      expect(message).toContain('complete')
    })

    it('should display correct message for delete action', () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'delete',
          items: mockItems,
        },
      })

      const message = wrapper.find('.warning-text').text()
      expect(message).toContain('delete')
      expect(message).toContain('items')
    })

    it('should display warning subtext for delete action', () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'delete',
          items: mockItems,
        },
      })

      expect(wrapper.find('.warning-subtext').text()).toBe('This action cannot be undone.')
    })

    it('should not display warning subtext for complete action', () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'complete',
          items: mockItems,
        },
      })

      expect(wrapper.find('.warning-subtext').exists()).toBe(false)
    })
  })

  describe('items list', () => {
    it('should display all items', () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'complete',
          items: mockItems,
        },
      })

      const itemCards = wrapper.findAll('.item-preview-card')
      expect(itemCards.length).toBe(2)
    })

    it('should display item details correctly', () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'complete',
          items: [mockItems[0]],
        },
      })

      expect(wrapper.text()).toContain('#1')
      expect(wrapper.text()).toContain('Test Item 1')
      expect(wrapper.text()).toContain('Description 1')
    })

    it('should display correct item count', () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'complete',
          items: mockItems,
        },
      })

      expect(wrapper.find('.items-list-title').text()).toContain('2 items')
    })

    it('should use singular form for single item', () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'complete',
          items: [mockItems[0]],
        },
      })

      expect(wrapper.find('.items-list-title').text()).toContain('1 item')
    })
  })

  describe('buttons', () => {
    it('should display correct confirm button text for complete', () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'complete',
          items: mockItems,
        },
      })

      const confirmButton = wrapper.findAll('.btn').find(btn => btn.text() === 'Mark Complete')
      expect(confirmButton.exists()).toBe(true)
    })

    it('should display correct confirm button text for delete', () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'delete',
          items: mockItems,
        },
      })

      const confirmButton = wrapper.findAll('.btn').find(btn => btn.text() === 'Delete Items')
      expect(confirmButton.exists()).toBe(true)
    })

    it('should disable buttons when processing', () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'complete',
          items: mockItems,
          isProcessing: true,
        },
      })

      const confirmButton = wrapper.find('.btn-success, .btn-danger')
      expect(confirmButton.attributes('disabled')).toBeDefined()
      expect(confirmButton.text()).toBe('Processing...')
    })

    it('should have correct button classes for complete action', () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'complete',
          items: mockItems,
        },
      })

      const confirmButton = wrapper.find('.btn-success')
      expect(confirmButton.exists()).toBe(true)
    })

    it('should have correct button classes for delete action', () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'delete',
          items: mockItems,
        },
      })

      const confirmButton = wrapper.find('.btn-danger')
      expect(confirmButton.exists()).toBe(true)
    })
  })

  describe('events', () => {
    it('should emit close event when close button is clicked', async () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'complete',
          items: mockItems,
        },
      })

      await wrapper.find('.close-btn').trigger('click')
      expect(wrapper.emitted('close')).toBeTruthy()
    })

    it('should emit close event when cancel button is clicked', async () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'complete',
          items: mockItems,
        },
      })

      await wrapper.find('.btn-secondary').trigger('click')
      expect(wrapper.emitted('close')).toBeTruthy()
    })

    it('should emit close event when modal backdrop is clicked', async () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'complete',
          items: mockItems,
        },
      })

      await wrapper.find('.modal').trigger('click')
      expect(wrapper.emitted('close')).toBeTruthy()
    })

    it('should emit confirm event when confirm button is clicked', async () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'complete',
          items: mockItems,
        },
      })

      await wrapper.find('.btn-success, .btn-danger').trigger('click')
      expect(wrapper.emitted('confirm')).toBeTruthy()
    })

    it('should not emit events when processing', async () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'complete',
          items: mockItems,
          isProcessing: true,
        },
      })

      await wrapper.find('.close-btn').trigger('click')
      await wrapper.find('.btn-success').trigger('click')

      expect(wrapper.emitted('close')).toBeFalsy()
      expect(wrapper.emitted('confirm')).toBeFalsy()
    })
  })

  describe('empty state', () => {
    it('should handle empty items array', () => {
      const wrapper = mount(BulkActionModal, {
        props: {
          isOpen: true,
          actionType: 'complete',
          items: [],
        },
      })

      expect(wrapper.find('.items-list-title').text()).toContain('0 items')
      expect(wrapper.findAll('.item-preview-card').length).toBe(0)
    })
  })
})
