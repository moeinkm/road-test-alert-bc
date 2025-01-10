import { Link } from 'react-router-dom';

interface AuthFooterProps {
  text: string;
  linkText: string;
  linkTo: string;
}

export function AuthFooter({ text, linkText, linkTo }: AuthFooterProps) {
  return (
    <p className="text-sm text-gray-600">
      {text}{' '}
      <Link
        to={linkTo}
        className="font-medium text-indigo-600 hover:text-indigo-500 hover:underline"
      >
        {linkText}
      </Link>
    </p>
  );
}