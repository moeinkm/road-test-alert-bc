import { XCircleIcon, CheckCircleIcon, ExclamationTriangleIcon } from '@heroicons/react/24/solid';

const styles = {
  success: 'bg-green-50 text-green-800 border-green-200',
  error: 'bg-red-50 text-red-800 border-red-200',
  warning: 'bg-yellow-50 text-yellow-800 border-yellow-200',
  info: 'bg-blue-50 text-blue-800 border-blue-200'
};

const icons = {
  success: <CheckCircleIcon className="h-5 w-5 text-green-400" aria-hidden="true" />,
  error: <XCircleIcon className="h-5 w-5 text-red-400" aria-hidden="true" />,
  warning: <ExclamationTriangleIcon className="h-5 w-5 text-yellow-400" aria-hidden="true" />,
  info: <CheckCircleIcon className="h-5 w-5 text-blue-400" aria-hidden="true" />
};

interface AlertProps {
  type: keyof typeof styles;
  message: string;
}

export function Alert({ type, message }: AlertProps) {
  return (
    <div className={`rounded-md p-4 border ${styles[type]}`} role="alert">
      <div className="flex">
        <div className="flex-shrink-0">
          {icons[type]}
        </div>
        <div className="ml-3">
          <p className="text-sm font-medium">{message}</p>
        </div>
      </div>
    </div>
  );
}