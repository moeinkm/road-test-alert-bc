import { PageMetadata } from '../components/common/PageMetadata';
import { metadata } from '../config/metadata';
import { PricingCard } from '../components/subscription/PricingCard';
import { packages } from '../data/packages';

export default function Packages() {
  return (
    <>
      <PageMetadata {...metadata.packages} />
      <div className="py-12 sm:py-16">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <div className="bg-green-50 border border-green-200 rounded-full px-4 py-1.5 inline-flex items-center mb-6">
            <span className="text-sm font-medium text-green-800">
              🎉 Special Offer: 50% OFF for First-Time Users
            </span>
          </div>
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
            Choose Your Package
          </h1>
          <p className="mt-6 text-lg leading-8 text-gray-600">
            Select the notification package that best fits your needs. All packages include our core features with varying durations.
          </p>
        </div>

        <div className="grid gap-8 max-w-7xl mx-auto sm:grid-cols-2 lg:grid-cols-4">
          {packages.map((pkg) => (
            <PricingCard key={pkg.id} pkg={pkg} />
          ))}
        </div>

        <div className="mt-12 text-center">
          <p className="text-sm text-gray-500">
            All prices in CAD. Packages auto-renew at regular price. Cancel anytime.
          </p>
        </div>
      </div>
    </>
  );
}