export class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public data?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export class AuthenticationError extends ApiError {
  constructor(message = 'Authentication required') {
    super(message, 401);
    this.name = 'AuthenticationError';
  }
}

export class ValidationError extends ApiError {
  constructor(message = 'Validation failed', data?: unknown) {
    super(message, 400, data);
    this.name = 'ValidationError';
  }
}