import { Link } from 'react-router-dom';
import { Logo } from '../brand/Logo';

interface FooterProps {
  className?: string;
}

const navigation = {
  main: [
    { name: 'Home', href: '/' },
    { name: 'Packages', href: '/packages' },
    { name: 'Privacy Policy', href: '/privacy' },
    { name: 'Terms', href: '/terms' }
  ],
};

export function Footer({ className = '' }: FooterProps) {
  return (
    <footer className={`bg-white mt-auto w-full ${className}`}>
      <div className="mx-auto max-w-7xl container-padding py-8 sm:py-12">
        <div className="flex justify-center">
          <Logo className="h-8" />
        </div>
        <nav className="mt-6 grid grid-cols-2 gap-6 sm:flex sm:justify-center sm:space-x-12" aria-label="Footer">
          {navigation.main.map((item) => (
            <div key={item.name}>
              <Link to={item.href} className="text-sm leading-6 text-gray-600 hover:text-gray-900">
                {item.name}
              </Link>
            </div>
          ))}
        </nav>
        <p className="mt-6 text-center text-xs leading-5 text-gray-500">
          &copy; {new Date().getFullYear()} ICBC Road Test Notifier. All rights reserved.
        </p>
      </div>
    </footer>
  );
}