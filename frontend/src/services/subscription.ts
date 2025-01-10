import { Package } from '../types';
import authService from './auth';

class SubscriptionService {
  private static instance: SubscriptionService;
  private readonly API_URL = '/api/subscriptions';
  private readonly SUBSCRIPTION_INTENT_KEY = 'subscriptionIntent';

  private constructor() {}

  public static getInstance(): SubscriptionService {
    if (!SubscriptionService.instance) {
      SubscriptionService.instance = new SubscriptionService();
    }
    return SubscriptionService.instance;
  }

  storeSubscriptionIntent(packageId: string): void {
    sessionStorage.setItem(this.SUBSCRIPTION_INTENT_KEY, packageId);
  }

  getSubscriptionIntent(): string | null {
    return sessionStorage.getItem(this.SUBSCRIPTION_INTENT_KEY);
  }

  clearSubscriptionIntent(): void {
    sessionStorage.removeItem(this.SUBSCRIPTION_INTENT_KEY);
  }

  async createSubscription(pkg: Package): Promise<{ clientSecret: string }> {
    const token = authService.getToken();
    if (!token) {
      throw new Error('Authentication required');
    }

    const response = await fetch(this.API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ packageId: pkg.id }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Failed to create subscription');
    }

    return response.json();
  }

  async getActiveSubscription(): Promise<Package | null> {
    const token = authService.getToken();
    if (!token) {
      return null;
    }

    try {
      const response = await fetch(`${this.API_URL}/active`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        return null;
      }

      return response.json();
    } catch (error) {
      console.error('Error fetching subscription:', error);
      return null;
    }
  }

  async cancelSubscription(): Promise<boolean> {
    const token = authService.getToken();
    if (!token) {
      throw new Error('Authentication required');
    }

    try {
      const response = await fetch(`${this.API_URL}/cancel`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to cancel subscription');
      }

      return true;
    } catch (error) {
      console.error('Error canceling subscription:', error);
      return false;
    }
  }
}

export default SubscriptionService.getInstance();