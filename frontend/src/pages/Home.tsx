import { useRef } from 'react';
import { PageMetadata } from '../components/common/PageMetadata';
import { metadata } from '../config/metadata';
import { NotificationForm } from '../components/notification/NotificationForm';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { CheckIcon } from '@heroicons/react/24/outline';

const features = [
  {
    title: 'Real-time Notifications',
    description: 'Get instant email alerts when road test slots become available at your preferred locations.'
  },
  {
    title: 'Multiple Locations',
    description: 'Monitor multiple ICBC test centers simultaneously to maximize your chances.'
  },
  {
    title: 'Flexible Scheduling',
    description: 'Choose your preferred days and date range for notifications.'
  },
  {
    title: 'Easy to Use',
    description: 'Simple setup process - just select your preferences and start receiving notifications.'
  }
];

export default function Home() {
  const formRef = useRef<HTMLDivElement>(null);

  const scrollToForm = () => {
    formRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <>
      <PageMetadata {...metadata.home} />
      
      {/* Hero Section */}
      <section className="relative isolate overflow-hidden bg-gradient-to-b from-indigo-100/20">
        <div className="mx-auto max-w-4xl px-6 py-24 sm:py-32 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
              Get Notified About ICBC Road Test Slots
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-600 max-w-2xl mx-auto">
              Never miss an available road test slot again. Get instant notifications when slots open up at your preferred ICBC locations.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Button onClick={scrollToForm} size="lg">
                Get Started
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {features.map((feature) => (
              <Card key={feature.title} className="h-full">
                <div className="flex flex-col h-full">
                  <div className="flex items-center gap-4 mb-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-100">
                      <CheckIcon className="h-6 w-6 text-indigo-600" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {feature.title}
                    </h3>
                  </div>
                  <p className="text-gray-600 flex-grow">
                    {feature.description}
                  </p>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Form Section */}
      <section ref={formRef} className="py-16 sm:py-24 bg-gray-50">
        <div className="mx-auto max-w-3xl px-6 lg:px-8">
          <NotificationForm />
        </div>
      </section>
    </>
  );
}