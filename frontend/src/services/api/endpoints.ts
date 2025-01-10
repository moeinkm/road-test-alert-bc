export const API_ENDPOINTS = {
  auth: {
    signin: '/auth/signin',
    signup: '/auth/signup',
    refresh: '/auth/refresh',
  },
  centers: {
    list: '/centers',
  },
  notifications: {
    preferences: '/notifications/preferences',
    unsubscribe: (id: string) => `/notifications/unsubscribe/${id}`,
  },
} as const;