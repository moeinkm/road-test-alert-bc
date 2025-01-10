import { ApiError, AuthenticationError, ValidationError } from './errors';

export class ApiClient {
  private static instance: ApiClient;
  private readonly baseUrl: string;

  private constructor() {
    this.baseUrl = import.meta.env.VITE_API_URL || '';
    console.log(this.baseUrl)
  }

  public static getInstance(): ApiClient {
    if (!ApiClient.instance) {
      ApiClient.instance = new ApiClient();
    }
    return ApiClient.instance;
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    const contentType = response.headers.get('content-type');
    const isJson = contentType?.includes('application/json');
    const data = isJson ? await response.json() : await response.text();

    if (!response.ok) {
      if (response.status === 401) {
        throw new AuthenticationError();
      }
      if (response.status === 400) {
        throw new ValidationError(data.detail || 'Validation failed', data);
      }
      throw new ApiError(
        data.detail || 'Request failed',
        response.status,
        data
      );
    }

    return data;
  }

  async get<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      method: 'GET',
    });
    return this.handleResponse<T>(response);
  }

  async post<T>(endpoint: string, data?: unknown, options: RequestInit = {}): Promise<T> {
    const body = data instanceof FormData ? data : JSON.stringify(data);
    const headers = data instanceof FormData ? {} : { 'Content-Type': 'application/json' };

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      method: 'POST',
      body,
      headers: {
        ...headers,
        ...options.headers,
      },
    });
    return this.handleResponse<T>(response);
  }
}