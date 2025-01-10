import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { PageMetadata } from '../components/common/PageMetadata';
import { AuthLayout } from '../components/auth/AuthLayout';
import { FormField } from '../components/form/FormField';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { Alert } from '../components/ui/Alert';
import { metadata } from '../config/metadata';
import { loginSchema } from '../utils/validation/auth';
import { authService } from '../services/auth';
import type { SignInFormData } from '../types/auth';

export default function Login() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const { register, handleSubmit, formState: { errors } } = useForm<SignInFormData>({
    resolver: zodResolver(loginSchema)
  });

  const onSubmit = async (data: SignInFormData) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await authService.signIn(data);
      if (result.success) {
        navigate('/preferences');
      } else {
        setError(result.message || 'Invalid email or password');
      }
    } catch (error) {
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <PageMetadata {...metadata.signIn} />
      <AuthLayout
        title="Sign in to your account"
        footerText="Don't have an account?"
        footerLinkText="Sign up"
        footerLinkTo="/signup"
      >
        {error && <Alert type="error" message={error} />}
        
        <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
          <FormField
            id="email"
            label="Email address"
            error={errors.email?.message}
          >
            <Input
              {...register('email')}
              id="email"
              type="email"
              autoComplete="email"
              error={!!errors.email}
              placeholder="Enter your email"
            />
          </FormField>

          <FormField
            id="password"
            label="Password"
            error={errors.password?.message}
          >
            <Input
              {...register('password')}
              id="password"
              type="password"
              autoComplete="current-password"
              error={!!errors.password}
              placeholder="Enter your password"
            />
          </FormField>

          <div className="flex items-center justify-between">
            <label className="flex items-center">
              <input
                {...register('rememberMe')}
                type="checkbox"
                className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              />
              <span className="ml-2 text-sm text-gray-600">Remember me</span>
            </label>

            <Button
              type="button"
              variant="link"
              onClick={() => navigate('/forgot-password')}
            >
              Forgot password?
            </Button>
          </div>

          <Button
            type="submit"
            fullWidth
            disabled={isLoading}
          >
            {isLoading ? 'Signing in...' : 'Sign in'}
          </Button>
        </form>
      </AuthLayout>
    </>
  );
}