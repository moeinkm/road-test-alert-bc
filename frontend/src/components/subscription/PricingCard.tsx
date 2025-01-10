import { Link } from 'react-router-dom';
import { CheckIcon, SparklesIcon } from '@heroicons/react/24/outline';
import { Card } from '../ui/Card';
import type { Package } from '../../types';

interface PricingCardProps {
  pkg: Package;
}

export function PricingCard({ pkg }: PricingCardProps) {
  return (
    <Card className={`flex flex-col justify-between relative ${pkg.popular ? 'border-indigo-600 shadow-lg' : ''}`}>
      {pkg.popular && (
        <div className="absolute -top-4 left-1/2 -translate-x-1/2">
          <span className="inline-flex items-center gap-1 rounded-full bg-indigo-600 px-4 py-1 text-sm font-medium text-white">
            <SparklesIcon className="h-4 w-4" />
            Most Popular
          </span>
        </div>
      )}

      <Card.Header>
        <div className="flex items-center justify-between">
          <div>
            <Card.Title className="text-xl">{pkg.name}</Card.Title>
            <p className="text-sm text-gray-600">{pkg.subtitle}</p>
          </div>
          <div className="text-right">
            <div className="flex flex-col items-end">
              <p className="text-3xl font-bold tracking-tight text-gray-900">
                ${pkg.discountedPrice}
              </p>
              <p className="text-sm text-gray-500 line-through">${pkg.price}</p>
              <p className="text-sm font-medium text-green-600">Save 50%</p>
            </div>
            <p className="text-sm text-gray-500">CAD</p>
          </div>
        </div>
        
        {pkg.description && (
          <p className="mt-4 text-sm text-gray-600">{pkg.description}</p>
        )}
        
        {pkg.highlight && (
          <div className="mt-4 rounded-md bg-indigo-50 p-2">
            <p className="text-sm font-medium text-indigo-700 text-center">
              {pkg.highlight}
            </p>
          </div>
        )}
      </Card.Header>

      <Card.Content>
        <ul role="list" className="mt-6 space-y-4">
          {pkg.features.map((feature) => (
            <li key={feature.text} className="flex gap-3">
              <CheckIcon 
                className={`h-6 w-5 flex-shrink-0 ${
                  feature.important ? 'text-green-600' : 'text-indigo-600'
                }`}
                aria-hidden="true"
              />
              <div>
                <p className={`text-sm ${feature.important ? 'font-medium text-green-900' : 'text-gray-600'}`}>
                  {feature.text}
                </p>
                {feature.description && (
                  <p className="text-xs text-gray-500 mt-0.5">
                    {feature.description}
                  </p>
                )}
              </div>
            </li>
          ))}
        </ul>
      </Card.Content>

      <Card.Footer className="mt-8">
        <Link
          to={`/subscribe/${pkg.id}`}
          className={`block w-full rounded-md px-3.5 py-2.5 text-center text-sm font-semibold text-white shadow-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 ${
            pkg.popular 
              ? 'bg-indigo-600 hover:bg-indigo-500 focus-visible:outline-indigo-600'
              : 'bg-gray-800 hover:bg-gray-700 focus-visible:outline-gray-800'
          }`}
        >
          Get Started
        </Link>
      </Card.Footer>
    </Card>
  );
}