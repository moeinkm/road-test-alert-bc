import { z } from 'zod';
import { loginSchema, signupSchema } from '../utils/validation/auth';

export type SignInFormData = z.infer<typeof loginSchema>;
export type SignupFormData = z.infer<typeof signupSchema>;

export interface AuthError {
  message: string;
}