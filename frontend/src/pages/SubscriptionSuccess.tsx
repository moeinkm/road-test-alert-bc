import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { CheckCircleIcon } from '@heroicons/react/24/outline';
import subscriptionService from '../services/subscription';

export default function SubscriptionSuccess() {
  return (
    <>
      <Helmet>
        <title>Subscription Success | Road Test Notifier BC</title>
      </Helmet>
      {/* Rest of the component content remains the same */}
    </>
  );
}