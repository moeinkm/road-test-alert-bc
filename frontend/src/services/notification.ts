import apiClient from './api/client';
import { API_ENDPOINTS } from './api/endpoints';
import type { UserPreferences } from '../types';

class NotificationService {
  private static instance: NotificationService;

  private constructor() {}

  public static getInstance(): NotificationService {
    if (!NotificationService.instance) {
      NotificationService.instance = new NotificationService();
    }
    return NotificationService.instance;
  }

  async updatePreferences(preferences: UserPreferences): Promise<boolean> {
    try {
      await apiClient.put(API_ENDPOINTS.notifications.preferences, preferences);
      return true;
    } catch (error) {
      console.error('Error updating preferences:', error);
      return false;
    }
  }

  async unsubscribe(notificationId: string): Promise<boolean> {
    try {
      await apiClient.post(API_ENDPOINTS.notifications.unsubscribe(notificationId));
      return true;
    } catch (error) {
      console.error('Error unsubscribing:', error);
      return false;
    }
  }
}

export default NotificationService.getInstance();