'use client';

import React, { useState } from 'react';
import authService from '@/services/authService';
import { useRouter } from 'next/navigation';

const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      await authService.register(username, email, password, firstName, lastName);

      // Automatically log in after registration
      const loginSuccess = await authService.login(username, password);

      if (loginSuccess) {
        router.push('/tasks');
      }
    } catch (err: any) {
      console.error('Registration error:', err);

      // Provide more specific error messages
      let errorMessage = 'Registration failed. ';

      if (err.message.includes('400')) {
        if (err.message.includes('Username already registered')) {
          errorMessage += 'This username is already taken. Please choose a different username.';
        } else if (err.message.includes('Email already registered')) {
          errorMessage += 'This email is already registered. Please use a different email or try logging in.';
        } else {
          errorMessage += 'Please check your information and try again.';
        }
      } else if (err.message.includes('server') || err.message.includes('fetch')) {
        errorMessage = 'Unable to connect to the server. Please make sure the backend API is running.';
      } else {
        errorMessage += 'Please check your information and try again.';
      }

      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="text-center mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginBottom: '1rem', color: 'var(--primary-color)' }}>
          <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
          <circle cx="9" cy="7" r="4"/>
          <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
        </svg>
        <h2 className="auth-title">Create Account</h2>
        <p className="text-muted">Join us to manage your tasks efficiently</p>
      </div>

      {error && <div className="error mb-3">{error}</div>}

      <form onSubmit={handleRegister}>
        <div className="form-group">
          <label htmlFor="firstName" className="form-label">First Name (Optional)</label>
          <input
            id="firstName"
            type="text"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            className="form-control"
            placeholder="Enter your first name"
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="lastName" className="form-label">Last Name (Optional)</label>
          <input
            id="lastName"
            type="text"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            className="form-control"
            placeholder="Enter your last name"
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="username" className="form-label">Username *</label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="form-control"
            placeholder="Choose a username"
            required
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="email" className="form-label">Email *</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="form-control"
            placeholder="Enter your email"
            required
            disabled={isLoading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="password" className="form-label">Password *</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="form-control"
            placeholder="Create a strong password (min 6 characters)"
            minLength={6}
            required
            disabled={isLoading}
          />
        </div>

        <button type="submit" className="btn btn-primary w-full" disabled={isLoading}>
          {isLoading ? (
            <>
              <div className="spinner" style={{ width: '16px', height: '16px' }}></div>
              Creating account...
            </>
          ) : (
            <>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: '0.5rem' }}>
                <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
              Create Account
            </>
          )}
        </button>
      </form>

      <div className="text-center mt-4">
        <p className="text-muted">
          Already have an account?{' '}
          <a href="/auth/login" className="btn btn-outline" style={{ padding: '0.25rem 0.5rem', fontSize: '0.875rem' }}>
            Login here
          </a>
        </p>
      </div>
    </div>
  );
};

export default RegisterPage;