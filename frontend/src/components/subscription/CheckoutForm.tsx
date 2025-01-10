import { useState } from 'react';
import { PaymentElement, useStripe, useElements } from '@stripe/react-stripe-js';
import { Button } from '../ui/Button';
import { Alert } from '../ui/Alert';
import type { Package } from '../../types';

interface CheckoutFormProps {
  selectedPackage: Package;
  onSuccess: () => void;
}

export function CheckoutForm({ selectedPackage, onSuccess }: CheckoutFormProps) {
  const stripe = useStripe();
  const elements = useElements();
  const [error, setError] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!stripe || !elements) {
      setError('Payment system is not ready. Please try again.');
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      const { error: submitError } = await stripe.confirmPayment({
        elements,
        confirmParams: {
          return_url: `${window.location.origin}/subscription/success`,
        },
      });

      if (submitError) {
        throw new Error(submitError.message || 'Payment failed');
      }

      onSuccess();
    } catch (error) {
      setError(error instanceof Error ? error.message : 'An unexpected error occurred');
      setIsProcessing(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && <Alert type="error" message={error} />}

      <div className="bg-gray-50 p-4 rounded-lg mb-4">
        <h3 className="text-lg font-medium text-gray-900 mb-2">Order Summary</h3>
        <div className="flex justify-between text-sm text-gray-600">
          <span>{selectedPackage.name}</span>
          <span>${selectedPackage.price} CAD</span>
        </div>
      </div>

      <PaymentElement />

      <Button
        type="submit"
        disabled={!stripe || isProcessing}
        fullWidth
      >
        {isProcessing ? 'Processing...' : `Pay $${selectedPackage.price} CAD`}
      </Button>

      <div className="mt-4 flex items-center justify-center space-x-2">
        <svg
          className="h-5 w-5 text-gray-400"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            fillRule="evenodd"
            d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
            clipRule="evenodd"
          />
        </svg>
        <span className="text-sm text-gray-500">
          Secure payment powered by Stripe
        </span>
      </div>
    </form>
  );
}