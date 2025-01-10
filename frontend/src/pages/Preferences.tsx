import { useState } from 'react';
import { Helmet } from 'react-helmet-async';
import { testCenters } from '../data/testCenters';

export default function Preferences() {
  const [selectedCenters, setSelectedCenters] = useState<string[]>([]);
  const [selectedDays, setSelectedDays] = useState<string[]>([]);
  const [notificationDays, setNotificationDays] = useState(15);

  return (
    <>
      <Helmet>
        <title>Preferences | Road Test Notifier BC</title>
      </Helmet>
      <div className="max-w-2xl mx-auto">
        {/* Rest of the component content remains the same */}
      </div>
    </>
  );
}