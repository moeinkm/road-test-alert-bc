import { ReactNode } from 'react';
import { Card } from '../../../components/ui/Card';

interface GuideSectionProps {
  children: ReactNode;
}

export function GuideSection({ children }: GuideSectionProps) {
  return (
    <Card className="overflow-hidden">
      {children}
    </Card>
  );
}