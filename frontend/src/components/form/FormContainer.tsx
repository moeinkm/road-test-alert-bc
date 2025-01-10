import { ReactNode } from 'react';
import { Card } from '../ui/Card';

interface FormContainerProps {
  title: string;
  children: ReactNode;
  footer?: ReactNode;
}

export function FormContainer({ title, children, footer }: FormContainerProps) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 container-padding">
      <Card className="w-full max-w-md space-y-8">
        <Card.Header>
          <Card.Title className="text-center text-2xl font-bold">
            {title}
          </Card.Title>
        </Card.Header>
        <Card.Content>
          {children}
        </Card.Content>
        {footer && (
          <Card.Footer className="flex justify-center">
            {footer}
          </Card.Footer>
        )}
      </Card>
    </div>
  );
}