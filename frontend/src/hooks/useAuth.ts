import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import authService from '../services/auth';

export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(authService.isAuthenticated());
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      if (!isAuthenticated && authService.getToken()) {
        const refreshed = await authService.refreshToken();
        setIsAuthenticated(refreshed);
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (email: string, password: string, rememberMe?: boolean) => {
    const result = await authService.login({ email, password, rememberMe });
    if (result.success) {
      setIsAuthenticated(true);
    }
    return result;
  };

  const logout = async () => {
    await authService.logout();
    setIsAuthenticated(false);
    navigate('/login');
  };

  return {
    isAuthenticated,
    isLoading,
    login,
    logout,
  };
}