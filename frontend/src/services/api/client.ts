import { ApiError, AuthenticationError, ValidationError } from './errors';

export class ApiClient {
  private static instance: ApiClient;
  private readonly baseUrl: string;

  private constructor() {
    this.baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/';
    console.log('API base URL:', this.baseUrl);
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
  if (!endpoint) {
    console.error('Endpoint is undefined or empty');
    throw new Error('Invalid endpoint');
  }

  const url = `${this.baseUrl}${endpoint}`;
  console.log('Sending GET request to:', url);

  const response = await fetch(url, {
    ...options,
    method: 'GET',
  });
  return this.handleResponse<T>(response);
}

  async post<T>(endpoint: string, data?: unknown, options: RequestInit = {}): Promise<T> {
    if (!endpoint) {
      console.error('Endpoint is undefined or empty');
      throw new Error('Invalid endpoint');
    }

    const body = data instanceof FormData ? data : JSON.stringify(data);
    const headers = data instanceof FormData ? {} : { 'Content-Type': 'application/json' };

    const url = `${this.baseUrl}${endpoint}`;
    console.log('Sending POST request to:', url);

    const response = await fetch(url, {
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