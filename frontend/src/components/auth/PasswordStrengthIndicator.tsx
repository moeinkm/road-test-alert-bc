import { useState, useEffect } from 'react';

interface PasswordStrengthIndicatorProps {
  password: string;
}

export function PasswordStrengthIndicator({ password }: PasswordStrengthIndicatorProps) {
  const [strength, setStrength] = useState({
    hasLength: false,
    hasUpperCase: false,
    hasLowerCase: false,
    hasNumber: false,
    hasSpecial: false,
  });

  useEffect(() => {
    setStrength({
      hasLength: password.length >= 8,
      hasUpperCase: /[A-Z]/.test(password),
      hasLowerCase: /[a-z]/.test(password),
      hasNumber: /[0-9]/.test(password),
      hasSpecial: /[^A-Za-z0-9]/.test(password),
    });
  }, [password]);

  const getColor = (isValid: boolean) => 
    isValid ? 'text-green-600' : 'text-gray-400';

  return (
    <div className="mt-2 text-sm">
      <p className={getColor(strength.hasLength)}>✓ At least 8 characters</p>
      <p className={getColor(strength.hasUpperCase)}>✓ One uppercase letter</p>
      <p className={getColor(strength.hasLowerCase)}>✓ One lowercase letter</p>
      <p className={getColor(strength.hasNumber)}>✓ One number</p>
      <p className={getColor(strength.hasSpecial)}>✓ One special character</p>
    </div>
  );
}