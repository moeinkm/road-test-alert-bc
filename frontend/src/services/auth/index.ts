import { AuthService } from './auth.service';
import { ApiClient } from '../api/client';

export const authService = new AuthService(ApiClient.getInstance());