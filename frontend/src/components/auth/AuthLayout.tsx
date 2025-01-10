import { ReactNode } from 'react';
import { FormContainer } from '../form/FormContainer';
import { AuthFooter } from './AuthFooter';

interface AuthLayoutProps {
  title: string;
  children: ReactNode;
  footerText: string;
  footerLinkText: string;
  footerLinkTo: string;
}

export function AuthLayout({
  title,
  children,
  footerText,
  footerLinkText,
  footerLinkTo,
}: AuthLayoutProps) {
  return (
    <FormContainer
      title={title}
      footer={
        <AuthFooter
          text={footerText}
          linkText={footerLinkText}
          linkTo={footerLinkTo}
        />
      }
    >
      {children}
    </FormContainer>
  );
}