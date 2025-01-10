import { Link } from 'react-router-dom';

interface LogoProps {
  className?: string;
}

export function Logo({ className = '' }: LogoProps) {
  return (
    <Link
      to="/"
      className={`flex items-center space-x-2 text-lg font-bold text-indigo-600 ${className}`}
      aria-label="Road Test Alert BC Home"
    >
      <svg
        className="h-8 w-8"
        viewBox="0 0 32 32"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <rect
          x="4"
          y="4"
          width="24"
          height="24"
          rx="6"
          className="fill-indigo-100"
        />
        <path
          d="M10 14.5C10 12.0147 12.0147 10 14.5 10C16.9853 10 19 12.0147 19 14.5C19 16.9853 16.9853 19 14.5 19"
          className="stroke-indigo-600"
          strokeWidth="2"
          strokeLinecap="round"
        />
        <path
          d="M14.5 14.5L22 22"
          className="stroke-indigo-600"
          strokeWidth="2"
          strokeLinecap="round"
        />
        <circle
          cx="14.5"
          cy="14.5"
          r="2"
          className="fill-indigo-600"
        />
      </svg>
      <span className="text-sm sm:text-base">Road Test Alert BC</span>
    </Link>
  );
}