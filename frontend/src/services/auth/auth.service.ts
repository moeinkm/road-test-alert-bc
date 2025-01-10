import { ApiClient } from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';
import type { SignInFormData, SignupFormData } from '../../types/auth';
import { ApiError } from '../api/errors';

export class AuthService {
  private readonly TOKEN_KEY = 'auth_token';
  private readonly REFRESH_TOKEN_KEY = 'refresh_token';

  constructor(private readonly api: ApiClient) {}

  private setTokens(accessToken: string, refreshToken?: string): void {
    localStorage.setItem(this.TOKEN_KEY, accessToken);
    if (refreshToken) {
      localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken);
    }
  }

  private clearTokens(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
  }

  public getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  public isAuthenticated(): boolean {
    return !!this.getToken();
  }

  async signup(data: SignupFormData): Promise<{ success: boolean; message?: string }> {
    try {
      const response = await this.api.post(API_ENDPOINTS.auth.signup, {
        email: data.email,
        full_name: data.fullName,
        password: data.password
      });

      if (response.access_token) {
        this.setTokens(response.access_token, response.refresh_token);
      }

      return { success: true };
    } catch (error) {
      console.error('Signup error:', error);
      if (error instanceof ApiError) {
        return {
          success: false,
          message: error.message
        };
      }
      throw error;
    }
  }

  async signIn(data: SignInFormData): Promise<{ success: boolean; message?: string }> {
    try {
      const formData = new FormData();
      formData.append('username', data.email);
      formData.append('password', data.password);

      const response = await this.api.post(API_ENDPOINTS.auth.signIn, formData);

      if (response.access_token) {
        this.setTokens(response.access_token, response.refresh_token);
        return { success: true };
      }

      return {
        success: false,
        message: 'Invalid credentials'
      };
    } catch (error) {
      console.error('Sign in error:', error);
      if (error instanceof ApiError) {
        return {
          success: false,
          message: error.message
        };
      }
      throw error;
    }
  }

  async refreshToken(): Promise<boolean> {
    const refreshToken = localStorage.getItem(this.REFRESH_TOKEN_KEY);
    if (!refreshToken) return false;

    try {
      const response = await this.api.post(API_ENDPOINTS.auth.refresh, { refresh_token: refreshToken });
      if (response.access_token) {
        this.setTokens(response.access_token);
        return true;
      }
      return false;
    } catch {
      this.clearTokens();
      return false;
    }
  }

  async logout(): Promise<void> {
    this.clearTokens();
  }
}