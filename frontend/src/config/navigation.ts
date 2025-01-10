import { HomeIcon, ArchiveBoxIcon, UserPlusIcon, BookOpenIcon } from '@heroicons/react/24/outline';
import { HomeIcon as HomeIconSolid, ArchiveBoxIcon as ArchiveBoxIconSolid, UserPlusIcon as UserPlusIconSolid, BookOpenIcon as BookOpenIconSolid } from '@heroicons/react/24/solid';
import type { NavigationItem } from '../types';

export const navigationItems: NavigationItem[] = [
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
    name: 'Package',
    href: '/packages',
    icon: ArchiveBoxIcon,
    activeIcon: ArchiveBoxIconSolid
  },
  {
    name: 'Sign Up',
    href: '/signup',
    icon: UserPlusIcon,
    activeIcon: UserPlusIconSolid
  }
];