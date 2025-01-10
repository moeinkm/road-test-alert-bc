import { z } from 'zod';
import { notificationSchema } from '../utils/validation/notification';

export type NotificationFormData = z.infer<typeof notificationSchema>;