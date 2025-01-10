import { useState } from 'react';

export default function SkipLink() {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <a
      href="#main-content"
      className={`
        fixed top-4 left-4 z-50 transform 
        ${isVisible ? 'translate-y-0' : '-translate-y-full'}
        bg-indigo-600 text-white px-4 py-2 rounded-md
        transition-transform duration-250 ease-in-out
        focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500
        focus:translate-y-0
      `}
      onFocus={() => setIsVisible(true)}
      onBlur={() => setIsVisible(false)}
    >
      Skip to main content
    </a>
  );
}