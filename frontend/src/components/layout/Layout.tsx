import { ReactNode } from 'react';
import { Navigation } from '../navigation/Navigation';
import { MobileNav } from '../navigation/MobileNav';
import { Footer } from './Footer';

interface LayoutProps {
  children: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navigation />
      <main className="flex-1 w-full container-padding pb-20 sm:pb-0">
        <div className="mx-auto max-w-7xl py-8">
          {children}
        </div>
      </main>
      <MobileNav />
      <Footer className="hidden sm:block" />
    </div>
  );
}