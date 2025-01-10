import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Elements } from '@stripe/react-stripe-js';
import { loadStripe } from '@stripe/stripe-js';
import { packages } from '../../data/packages';
import { CheckoutForm } from './CheckoutForm';
import { FormContainer } from '../form/FormContainer';
import { Alert } from '../ui/Alert';
import subscriptionService from '../../services/subscription';
import authService from '../../services/auth';

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY);

export default function Subscribe() {
  const { packageId } = useParams<{ packageId: string }>();
  const navigate = useNavigate();
  const [clientSecret, setClientSecret] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const selectedPackage = packages.find(p => p.id === packageId);

  useEffect(() => {
    const initSubscription = async () => {
      if (!selectedPackage) {
        setError('Invalid package selected');
        return;
      }

      try {
        const { clientSecret } = await subscriptionService.createSubscription(selectedPackage);
        setClientSecret(clientSecret);
      } catch (err) {
        setError('Failed to initialize payment. Please try again.');
      }
    };

    if (!authService.isAuthenticated()) {
      subscriptionService.storeSubscriptionIntent(packageId!);
      navigate('/login');
      return;
    }

    initSubscription();
  }, [packageId, selectedPackage, navigate]);

  if (!selectedPackage) {
    return <Alert type="error" message="Invalid package selected" />;
  }

  if (!clientSecret) {
    return <div>Loading...</div>;
  }

  return (
    <FormContainer title={`Subscribe to ${selectedPackage.name}`}>
      {error ? (
        <Alert type="error" message={error} />
      ) : (
        <Elements
          stripe={stripePromise}
          options={{
            clientSecret,
            appearance: {
              theme: 'stripe',
              variables: {
                colorPrimary: '#4F46E5',
              },
            },
          }}
        >
          <CheckoutForm
            selectedPackage={selectedPackage}
            onSuccess={() => navigate('/subscription/success')}
          />
        </Elements>
      )}
    </FormContainer>
  );
}