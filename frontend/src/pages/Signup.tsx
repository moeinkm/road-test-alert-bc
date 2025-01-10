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
import { signupSchema } from '../utils/validation/auth';
import { PasswordStrengthIndicator } from '../components/auth';
import { authService } from '../services/auth';
import type { SignupFormData } from '../types/auth';

export default function Signup() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const { register, handleSubmit, watch, formState: { errors } } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema)
  });

  const password = watch('password', '');

  const onSubmit = async (data: SignupFormData) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await authService.signup(data);
      if (result.success) {
        navigate('/packages');
      } else {
        setError(result.message || 'Failed to create account. Please try again.');
      }
    } catch (error) {
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <PageMetadata {...metadata.signUp} />
      <AuthLayout
        title="Create your account"
        footerText="Already have an account?"
        footerLinkText="Sign in"
        footerLinkTo="/login"
      >
        {error && <Alert type="error" message={error} />}
        
        <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
          <FormField
            id="fullName"
            label="Full name"
            error={errors.fullName?.message}
          >
            <Input
              {...register('fullName')}
              id="fullName"
              type="text"
              autoComplete="name"
              error={!!errors.fullName}
              placeholder="Enter your full name"
            />
          </FormField>

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
              autoComplete="new-password"
              error={!!errors.password}
              placeholder="Create a password"
            />
            <PasswordStrengthIndicator password={password} />
          </FormField>

          <FormField
            id="confirmPassword"
            label="Confirm password"
            error={errors.confirmPassword?.message}
          >
            <Input
              {...register('confirmPassword')}
              id="confirmPassword"
              type="password"
              autoComplete="new-password"
              error={!!errors.confirmPassword}
              placeholder="Confirm your password"
            />
          </FormField>

          <div className="flex items-center">
            <input
              {...register('acceptTerms')}
              id="acceptTerms"
              type="checkbox"
              className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
            />
            <label htmlFor="acceptTerms" className="ml-2 text-sm text-gray-600">
              I agree to the{' '}
              <Button
                variant="link"
                onClick={() => navigate('/terms')}
              >
                Terms of Service
              </Button>
              {' '}and{' '}
              <Button
                variant="link"
                onClick={() => navigate('/privacy')}
              >
                Privacy Policy
              </Button>
            </label>
          </div>
          {errors.acceptTerms && (
            <p className="text-sm text-red-500">{errors.acceptTerms.message}</p>
          )}

          <Button
            type="submit"
            fullWidth
            disabled={isLoading}
          >
            {isLoading ? 'Creating account...' : 'Create account'}
          </Button>
        </form>
      </AuthLayout>
    </>
  );
}