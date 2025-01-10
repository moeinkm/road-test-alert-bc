export const APP_NAME = 'Road Test Alert BC';

export const createPageTitle = (pageTitle: string) => `${pageTitle} | ${APP_NAME}`;

export const metadata = {
  home: {
    title: createPageTitle('Home'),
    description: 'Get instant notifications for ICBC road test slots at your preferred locations.',
  },
  signIn: {
    title: createPageTitle('Sign In'),
    description: 'Sign in to your Road Test Alert BC account.',
  },
  signUp: {
    title: createPageTitle('Sign Up'),
    description: 'Create your Road Test Alert BC account.',
  },
  packages: {
    title: createPageTitle('Packages'),
    description: 'Choose your perfect notification package.',
  },
  preferences: {
    title: createPageTitle('Preferences'),
    description: 'Customize your road test notification preferences.',
  },
  subscribe: {
    title: createPageTitle('Subscribe'),
    description: 'Subscribe to road test notifications.',
  },
  subscriptionSuccess: {
    title: createPageTitle('Subscription Success'),
    description: 'Your subscription has been confirmed.',
  },
} as const;