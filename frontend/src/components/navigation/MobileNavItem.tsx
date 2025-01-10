import { Link } from 'react-router-dom';
import type { IconType } from '../../types';

interface MobileNavItemProps {
  name: string;
  href: string;
  Icon: IconType;
  ActiveIcon: IconType;
  isActive: boolean;
}

export function MobileNavItem({ name, href, Icon, ActiveIcon, isActive }: MobileNavItemProps) {
  const IconComponent = isActive ? ActiveIcon : Icon;
  
  return (
    <Link
      to={href}
      className={`
        flex flex-col items-center justify-center w-20 h-full py-1
        transition-colors duration-200
        ${isActive ? 'text-indigo-600' : 'text-gray-600 hover:text-indigo-600 active:text-indigo-600'}
      `}
    >
      <IconComponent className="h-6 w-6" aria-hidden="true" />
      <span className="mt-1 text-xs font-medium">{name}</span>
    </Link>
  );
}