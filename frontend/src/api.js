import axios from 'axios'

// Use relative URL to leverage Vite proxy configuration
const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url, config.params)
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url)
    return response
  },
  (error) => {
    console.error('API Response Error:', {
      message: error.message,
      url: error.config?.url,
      status: error.response?.status,
      data: error.response?.data,
      code: error.code,
    })
    return Promise.reject(error)
  }
)

export const itemService = {
  // Get all items with filters
  getAll(params = {}) {
    return api.get('/items/', { params })
  },

  // Get a single item by ID
  get(id) {
    return api.get(`/items/${id}/`)
  },

  // Create a new item
  create(data) {
    return api.post('/items/', data)
  },

  // Update an existing item
  update(id, data) {
    return api.put(`/items/${id}/`, data)
  },

  // Partial update an existing item
  patch(id, data) {
    return api.patch(`/items/${id}/`, data)
  },

  // Delete an item
  delete(id) {
    return api.delete(`/items/${id}/`)
  },

  // Bulk delete
  bulkDelete(ids) {
    return Promise.all(ids.map(id => api.delete(`/items/${id}/`)))
  },

  // Bulk update (uses PATCH for partial updates)
  bulkUpdate(ids, data) {
    return Promise.all(ids.map(id => api.patch(`/items/${id}/`, data)))
  },

  // Get statistics
  getStats() {
    return api.get('/items/stats/')
  },
}

export default api
