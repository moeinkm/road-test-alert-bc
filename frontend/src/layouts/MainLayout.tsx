import { ReactNode } from 'react';
import { Navigation } from '../components/navigation/Navigation';
import { MobileNav } from '../components/navigation/MobileNav';
import { Footer } from '../components/layout/Footer';

interface MainLayoutProps {
  children: ReactNode;
}

export function MainLayout({ children }: MainLayoutProps) {
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