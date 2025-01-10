import { UseFormRegister } from 'react-hook-form';
import { FormField } from '../form/FormField';
import { Card } from '../ui/Card';
import type { City } from '../../types/center';
import type { NotificationFormData } from '../../types/notification';

interface CitySelectProps {
  cities: City[];
  register: UseFormRegister<NotificationFormData>;
  error?: string;
}

export function CitySelect({ cities, register, error }: CitySelectProps) {
  return (
    <FormField
      id="centers"
      label="Test Centers"
      error={error}
    >
      <div className="space-y-6">
        {cities.map((city) => (
          <Card key={city.name} className="overflow-hidden">
            <Card.Header className="bg-gray-50 py-3">
              <h3 className="font-medium text-gray-900">{city.name}</h3>
            </Card.Header>
            <Card.Content className="grid gap-4 sm:grid-cols-2">
              {city.centers.map((center) => (
                <label
                  key={center.id}
                  className="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <input
                    type="checkbox"
                    value={center.id}
                    {...register('centers')}
                    className="mt-1 h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                  />
                  <div>
                    <p className="text-sm font-medium text-gray-900">{center.name}</p>
                    <p className="text-sm text-gray-500">{center.address}</p>
                  </div>
                </label>
              ))}
            </Card.Content>
          </Card>
        ))}
      </div>
    </FormField>
  );
}