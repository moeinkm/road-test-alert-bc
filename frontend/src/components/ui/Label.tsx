import { LabelHTMLAttributes } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';

const labelVariants = cva(
  'text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70',
  {
    variants: {
      variant: {
        default: 'text-gray-700',
        error: 'text-red-500',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

interface LabelProps
  extends LabelHTMLAttributes<HTMLLabelElement>,
    VariantProps<typeof labelVariants> {
  error?: boolean;
}

export function Label({ className, error, ...props }: LabelProps) {
  return (
    <label
      className={labelVariants({
        variant: error ? 'error' : 'default',
        className,
      })}
      {...props}
    />
  );
}