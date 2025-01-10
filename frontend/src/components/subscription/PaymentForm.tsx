import { useState } from 'react';
import { useStripe, useElements, PaymentElement } from '@stripe/react-stripe-js';
import { Package } from '../../types';
import { Alert } from '../ui/Alert';

interface PaymentFormProps {
  selectedPackage: Package;
  onSuccess: () => void;
}

export default function PaymentForm({ selectedPackage, onSuccess }: PaymentFormProps) {
  const stripe = useStripe();
  const elements = useElements();
  const [error, setError] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!stripe || !elements) {
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
        setError(submitError.message || 'Payment failed');
      } else {
        onSuccess();
      }
    } catch (e) {
      setError('An unexpected error occurred');
    } finally {
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
          <span>${selectedPackage.price}</span>
        </div>
      </div>

      <PaymentElement />

      <div className="flex items-center">
        <input
          id="save-payment"
          type="checkbox"
          className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
        />
        <label htmlFor="save-payment" className="ml-2 block text-sm text-gray-900">
          Save payment method for future use
        </label>
      </div>

      <button
        type="submit"
        disabled={!stripe || isProcessing}
        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
      >
        {isProcessing ? 'Processing...' : `Pay $${selectedPackage.price}`}
      </button>

      <div className="mt-4 flex items-center justify-center space-x-2">
        <img src="/secure-stripe.svg" alt="Secure payments by Stripe" className="h-8" />
        <div className="text-sm text-gray-500">
          Secure payment powered by Stripe
        </div>
      </div>
    </form>
  );
}