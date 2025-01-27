export const API_ENDPOINTS = {
  auth: {
    signIn: '/api/v1/auth/signin',
    signup: '/api/v1/auth/signup',
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