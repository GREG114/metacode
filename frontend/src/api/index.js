import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 数据模型 API
export const modelApi = {
  list: () => api.get('/models/'),
  get: (id) => api.get(`/models/${id}/`),
  create: (data) => api.post('/models/', data),
  update: (id, data) => api.put(`/models/${id}/`, data),
  delete: (id) => api.delete(`/models/${id}/`),
  getForm: (id) => api.get(`/models/${id}/form/`)
}

// 表单数据 API
export const formDataApi = {
  list: (modelId) => api.get(`/form-data/?model=${modelId}`),
  create: (data) => api.post('/form-data/', data),
  delete: (id) => api.delete(`/form-data/${id}/`)
}

// 布局 API
export const layoutApi = {
  list: (modelId) => api.get(`/layouts/?model=${modelId}`),
  get: (id) => api.get(`/layouts/${id}/`),
  create: (data) => api.post('/layouts/', data),
  update: (id, data) => api.put(`/layouts/${id}/`, data),
  delete: (id) => api.delete(`/layouts/${id}/`),
  activate: (id) => api.post(`/layouts/${id}/activate/`),
  duplicate: (id, data) => api.post(`/layouts/${id}/duplicate/`, data)
}

export default api