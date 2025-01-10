import { ReactNode } from 'react';
import { Label } from '../ui/Label';

interface FormFieldProps {
  id: string;
  label: string;
  error?: string;
  children: ReactNode;
}

export function FormField({ id, label, error, children }: FormFieldProps) {
  return (
    <div className="space-y-2">
      <Label htmlFor={id} error={!!error}>
        {label}
      </Label>
      {children}
      {error && (
        <p className="text-sm text-red-500">{error}</p>
      )}
    </div>
  );
}