import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Session cookies göndermek için - ÖNEMLİ!
});

// CSRF token al
const getCsrfToken = () => {
  const name = 'csrftoken';
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

// Token ekle
api.interceptors.request.use((config) => {
  // CSRF token ekle (POST, PUT, PATCH, DELETE için)
  if (['post', 'put', 'patch', 'delete'].includes(config.method.toLowerCase())) {
    const csrfToken = getCsrfToken();
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken;
      console.log('CSRF Token sent');
    }
  }
  
  return config;
});

// Users API
export const usersAPI = {
  register: (data) => api.post('/users/register/', data),
  login: (username, password) => api.post('/users/login/', { username, password }),
  getProfile: () => api.get('/users/me/'),
  updateProfile: (data) => api.patch('/users/me/', data, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  changePassword: (data) => api.post('/users/change_password/', data),
};

// Workshops API
export const workshopsAPI = {
  getCategories: () => api.get('/workshops/categories/'),
  getWorkshops: (params) => api.get('/workshops/', { params }),
  getWorkshop: (id) => api.get(`/workshops/${id}/`),
  myWorkshops: () => api.get('/workshops/my_workshops/'),
  createWorkshop: (data) => api.post('/workshops/', data),
  updateWorkshop: (id, data) => api.patch(`/workshops/${id}/`, data),
};

// Reviews API
export const reviewsAPI = {
  getReviews: (workshopId) => {
    if (workshopId) {
      return api.get('/reviews/', { params: { workshop: workshopId } });
    }
    return api.get('/reviews/');
  },
  createReview: (workshopId, data) => api.post('/reviews/', data, { params: { workshop: workshopId } }),
  replyReview: (reviewId, data) => api.post(`/reviews/${reviewId}/reply/`, data),
};

// Messaging API
export const messagingAPI = {
  getConversations: () => api.get('/messaging/conversations/'),
  getConversation: (id) => api.get(`/messaging/conversations/${id}/`),
  startConversation: (data) => api.post('/messaging/conversations/start_conversation/', data),
  sendMessage: (conversationId, data) => api.post(`/messaging/conversations/${conversationId}/send_message/`, data),
  markAsRead: (conversationId) => api.post(`/messaging/conversations/${conversationId}/mark_as_read/`),
};

// Favorites API
export const favoritesAPI = {
  getFavorites: () => api.get('/users/favorites/'),
  addFavorite: (workshopId) => api.post('/users/favorites/', { workshop: workshopId }),
  removeFavorite: (favoriteId) => api.delete(`/users/favorites/${favoriteId}/`),
};

// Inventory API - Yeni Stok Yönetimi
export const inventoryAPI = {
  // Araçlar
  getVehicles: (params) => api.get('/inventory/vehicles/', { params }),
  createVehicle: (data) => api.post('/inventory/vehicles/', data),
  
  // Kategoriler
  getCategories: () => api.get('/inventory/categories/'),
  
  // Parçalar
  getParts: (params) => api.get('/inventory/parts/', { params }),
  getPart: (id) => api.get(`/inventory/parts/${id}/`),
  createPart: (data) => api.post('/inventory/parts/', data),
  updatePart: (id, data) => api.patch(`/inventory/parts/${id}/`, data),
  deletePart: (id) => api.delete(`/inventory/parts/${id}/`),
  getLowStockParts: () => api.get('/inventory/parts/low_stock/'),
  
  // Parça işlemleri
  addVehicleToPart: (partId, vehicleId) => api.post(`/inventory/parts/${partId}/add_vehicle/`, { vehicle_id: vehicleId }),
  addAlternativeToPart: (partId, alternativeId, note) => api.post(`/inventory/parts/${partId}/add_alternative/`, { alternative_id: alternativeId, note }),
  addNoteToPart: (partId, note) => api.post(`/inventory/parts/${partId}/add_note/`, { note }),
  addPurchasePrice: (partId, data) => api.post(`/inventory/parts/${partId}/add_purchase_price/`, data),
  addSalePrice: (partId, data) => api.post(`/inventory/parts/${partId}/add_sale_price/`, data),
  stockMovement: (partId, data) => api.post(`/inventory/parts/${partId}/stock_movement/`, data),
  
  // Arama
  search: (query) => api.get('/inventory/search/search/', { params: { q: query } }),
};

// Payments API
export const paymentsAPI = {
  getPlans: () => api.get('/payments/plans/'),
  getSubscriptions: () => api.get('/payments/subscriptions/'),
  subscribe: (data) => api.post('/payments/subscriptions/subscribe/', data),
  cancelSubscription: (id) => api.post(`/payments/subscriptions/${id}/cancel/`),
  getInvoices: () => api.get('/payments/invoices/'),
};

export default api;
