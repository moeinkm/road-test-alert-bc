import { Link } from 'react-router-dom';

interface NavLinkProps {
  to: string;
  children: React.ReactNode;
  className?: string;
  'aria-current'?: 'page' | undefined;
}

export function NavLink({ to, children, className = '', ...props }: NavLinkProps) {
  return (
    <Link
      to={to}
      className={`
        relative
        inline-flex items-center px-1 pt-1 text-sm font-medium
        transition-all duration-250 ease-in-out
        group
        ${className}
      `}
      {...props}
    >
      {children}
      <span 
        className={`
          absolute -bottom-1 left-0 h-[2px] w-0
          transition-all duration-300 ease-in-out
          group-hover:w-full
          ${className.includes('text-indigo-600') ? 'bg-indigo-600' : 'bg-gray-900 group-hover:bg-indigo-600'}
        `}
      />
    </Link>
  );
}