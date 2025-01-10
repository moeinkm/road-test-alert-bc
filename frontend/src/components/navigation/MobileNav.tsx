import { useLocation } from 'react-router-dom';
import { HomeIcon, BookOpenIcon, ArchiveBoxIcon, UserIcon } from '@heroicons/react/24/outline';
import { HomeIcon as HomeIconSolid, BookOpenIcon as BookOpenIconSolid, ArchiveBoxIcon as ArchiveBoxIconSolid, UserIcon as UserIconSolid } from '@heroicons/react/24/solid';
import { MobileNavItem } from './MobileNavItem';

const navigationItems = [
  {
    name: 'Home',
    href: '/',
    icon: HomeIcon,
    activeIcon: HomeIconSolid
  },
  {
    name: 'Guides',
    href: '/guides',
    icon: BookOpenIcon,
    activeIcon: BookOpenIconSolid
  },
  {
    name: 'Packages',
    href: '/packages',
    icon: ArchiveBoxIcon,
    activeIcon: ArchiveBoxIconSolid
  },
  {
    name: 'Sign In',
    href: '/login',
    icon: UserIcon,
    activeIcon: UserIconSolid
  }
];

export function MobileNav() {
  const location = useLocation();

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 block md:hidden" aria-label="Mobile navigation">
      <div className="bg-white border-t border-gray-200 shadow-lg px-6">
        <div className="flex h-16 justify-around items-center max-w-md mx-auto">
          {navigationItems.map((item) => (
            <MobileNavItem
              key={item.name}
              name={item.name}
              href={item.href}
              Icon={item.icon}
              ActiveIcon={item.activeIcon}
              isActive={location.pathname === item.href}
            />
          ))}
        </div>
      </div>
    </nav>
  );
}