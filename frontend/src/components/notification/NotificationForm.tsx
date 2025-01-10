import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { FormField } from '../form/FormField';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';
import { Alert } from '../ui/Alert';
import { Card } from '../ui/Card';
import { CitySelect } from './CitySelect';
import { DaySelect } from './DaySelect';
import { notificationSchema } from '../../utils/validation/notification';
import { centersService } from '../../services/centers';
import { DAYS } from '../../constants/days';
import type { City } from '../../types/center';
import type { NotificationFormData } from '../../types/notification';

export function NotificationForm() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [cities, setCities] = useState<City[]>([]);

  const today = new Date().toISOString().split('T')[0];

  const { register, handleSubmit, formState: { errors } } = useForm<NotificationFormData>({
    resolver: zodResolver(notificationSchema),
    defaultValues: {
      startDate: today,
      days: DAYS.map(day => day.value)
    }
  });

  useEffect(() => {
    const loadCenters = async () => {
      try {
        const centers = await centersService.getCenters();
        const groupedByCity = centers.reduce((acc, center) => {
          const city = acc.find(c => c.name === center.city);
          if (city) {
            city.centers.push(center);
          } else {
            acc.push({ name: center.city, centers: [center] });
          }
          return acc;
        }, [] as City[]);
        
        setCities(groupedByCity.sort((a, b) => a.name.localeCompare(b.name)));
      } catch (error) {
        setError('Failed to load test centers');
      }
    };

    loadCenters();
  }, []);

  const onSubmit = async (data: NotificationFormData) => {
    setIsLoading(true);
    setError(null);

    try {
      // TODO: Implement notification preferences submission
      console.log('Form data:', data);
    } catch (error) {
      setError('Failed to save preferences');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card>
      <Card.Header>
        <Card.Title className="text-2xl">Set Your Notification Preferences</Card.Title>
        <p className="mt-2 text-gray-600">
          Choose your preferred test centers and availability to receive notifications.
        </p>
      </Card.Header>

      <Card.Content>
        {error && <Alert type="error" message={error} className="mb-6" />}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
          <FormField
            id="email"
            label="Email Address"
            error={errors.email?.message}
          >
            <Input
              {...register('email')}
              type="email"
              placeholder="Enter your email address"
              error={!!errors.email}
            />
          </FormField>

          <CitySelect
            cities={cities}
            register={register}
            error={errors.centers?.message}
          />

          <div className="grid gap-6 sm:grid-cols-2">
            <FormField
              id="startDate"
              label="Start Date"
              error={errors.startDate?.message}
            >
              <Input
                {...register('startDate')}
                type="date"
                defaultValue={today}
                min={today}
                error={!!errors.startDate}
              />
            </FormField>

            <FormField
              id="endDate"
              label="End Date"
              error={errors.endDate?.message}
            >
              <Input
                {...register('endDate')}
                type="date"
                min={today}
                error={!!errors.endDate}
              />
            </FormField>
          </div>

          <DaySelect
            register={register}
            error={errors.days?.message}
            defaultSelectedDays={DAYS.map(day => day.value)}
          />

          <Button
            type="submit"
            fullWidth
            size="lg"
            disabled={isLoading}
          >
            {isLoading ? 'Saving...' : 'Send me email when available'}
          </Button>
        </form>
      </Card.Content>
    </Card>
  );
}