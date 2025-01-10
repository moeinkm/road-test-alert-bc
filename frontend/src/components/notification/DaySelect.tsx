import { UseFormRegister } from 'react-hook-form';
import { FormField } from '../form/FormField';
import { Card } from '../ui/Card';
import { DAYS } from '../../constants/days';
import type { NotificationFormData } from '../../types/notification';

interface DaySelectProps {
  register: UseFormRegister<NotificationFormData>;
  error?: string;
  defaultSelectedDays?: string[];
}

export function DaySelect({ register, error, defaultSelectedDays }: DaySelectProps) {
  return (
    <FormField
      id="days"
      label="Preferred Days"
      error={error}
    >
      <Card>
        <Card.Content className="grid gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
          {DAYS.map((day) => (
            <label
              key={day.value}
              className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <input
                type="checkbox"
                value={day.value}
                defaultChecked={defaultSelectedDays?.includes(day.value)}
                {...register('days')}
                className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              />
              <span className="text-sm font-medium text-gray-900">{day.label}</span>
            </label>
          ))}
        </Card.Content>
      </Card>
    </FormField>
  );
}