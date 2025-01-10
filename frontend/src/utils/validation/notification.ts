import { z } from 'zod';
import { emailSchema } from './common';

export const notificationSchema = z.object({
  email: emailSchema,
  centers: z.array(z.number())
    .min(1, 'Please select at least one test center'),
  startDate: z.string()
    .min(1, 'Start date is required'),
  endDate: z.string()
    .min(1, 'End date is required'),
  days: z.array(z.string())
    .min(1, 'Please select at least one day'),
}).refine((data) => {
  const start = new Date(data.startDate);
  const end = new Date(data.endDate);
  return end >= start;
}, {
  message: "End date must be after start date",
  path: ["endDate"],
});