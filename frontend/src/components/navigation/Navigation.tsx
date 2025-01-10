import { Link } from 'react-router-dom';
import { NavLink } from './NavLink';
import { Logo } from '../brand/Logo';

const mainNavigation = [
  { name: 'Home', href: '/' },
  { name: 'Guides', href: '/guides' },
  { name: 'Packages', href: '/packages' }
];

const authNavigation = [
  { name: 'Sign In', href: '/login' },
  { name: 'Sign Up', href: '/signup' }
];

export function Navigation() {
  return (
    <nav aria-label="Main navigation" className="bg-white shadow-sm">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 justify-between">
          <div className="flex items-center">
            <Logo />
            {/* Show navigation on tablet and up, hide on mobile */}
            <div className="hidden md:ml-6 md:flex md:space-x-8">
              {mainNavigation.map((item) => (
                <NavLink
                  key={item.name}
                  to={item.href}
                  className="text-gray-900 hover:text-indigo-600"
                >
                  {item.name}
                </NavLink>
              ))}
            </div>
          </div>
          {/* Show auth navigation on tablet and up, hide on mobile */}
          <div className="hidden md:flex md:items-center md:space-x-8">
            {authNavigation.map((item) => (
              <NavLink
                key={item.name}
                to={item.href}
                className="text-gray-900 hover:text-indigo-600"
              >
                {item.name}
              </NavLink>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
}