export function sanitizeInput(input: string): string {
  return input.replace(/[<>]/g, '');
}

export function validateCSRFToken(token: string): boolean {
  // Implement CSRF token validation
  return token.length > 0;
}

export const securityHeaders = {
  'Content-Security-Policy': "default-src 'self'; script-src 'self' https://js.stripe.com; frame-src https://js.stripe.com;",
  'X-Frame-Options': 'DENY',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'geolocation=(), microphone=()',
};