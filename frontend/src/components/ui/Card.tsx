import { HTMLAttributes, ReactNode } from 'react';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
}

export function Card({ children, className, ...props }: CardProps) {
  return (
    <div
      className={`rounded-lg border border-gray-200 bg-white p-6 shadow-sm ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

Card.Header = function CardHeader({
  children,
  className,
  ...props
}: CardProps) {
  return (
    <div
      className={`flex flex-col space-y-1.5 pb-4 ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

Card.Title = function CardTitle({
  children,
  className,
  ...props
}: CardProps) {
  return (
    <h3
      className={`text-lg font-semibold leading-none tracking-tight ${className}`}
      {...props}
    >
      {children}
    </h3>
  );
};

Card.Content = function CardContent({
  children,
  className,
  ...props
}: CardProps) {
  return (
    <div className={`pt-0 ${className}`} {...props}>
      {children}
    </div>
  );
};

Card.Footer = function CardFooter({
  children,
  className,
  ...props
}: CardProps) {
  return (
    <div
      className={`flex items-center pt-4 ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};