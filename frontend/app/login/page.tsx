/**
 * Login page
 * References: Task T227, Spec §X
 */
'use client';

import { useState } from 'react';
import LoginForm from '@/components/LoginForm';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleLogin = async (formData: { email: string; password: string }) => {
    setLoading(true);
    setError('');

    try {
      // In a real application, you would call your backend API here
      // For now, we'll just simulate the API call
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Store the JWT token in localStorage (or use a more secure method in production)
        localStorage.setItem('token', data.data.token);

        // Add a small delay before redirect to ensure the token is properly stored
        // This can help with potential header size issues
        await new Promise(resolve => setTimeout(resolve, 100));

        // Redirect to dashboard after successful login
        router.push('/');
      } else {
        setError(data.error || 'Login failed. Please try again.');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <LoginForm onLogin={handleLogin} loading={loading} error={error} />
        <div className="text-center mt-4">
          <p className="text-sm text-gray-600">
            Don't have an account?{' '}
            <a href="/signup" className="font-medium text-indigo-600 hover:text-indigo-500">
              Sign up
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}