class AuthService {
  private API_BASE_URL: string;

  constructor() {
    this.API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://sz453781it-hackathon-todo.hf.space';
    console.log('AuthService initialized with API_BASE_URL:', this.API_BASE_URL);
  }

  async login(username: string, password: string): Promise<boolean> {
    try {
      console.log('Attempting login to:', `${this.API_BASE_URL}/api/v1/auth/login`, 'with data:', { username, password: '***' });
      const response = await fetch(`${this.API_BASE_URL}/api/v1/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      console.log('Login response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Login error response:', errorText);
        throw new Error(`Login failed: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      console.log('Login successful, token received:', { hasToken: !!data.access_token });

      // Store the token in localStorage
      if (data.access_token) {
        localStorage.setItem('access_token', data.access_token);
        return true;
      }

      return false;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  async register(username: string, email: string, password: string, firstName?: string, lastName?: string): Promise<boolean> {
    try {
      console.log('Attempting registration to:', `${this.API_BASE_URL}/api/v1/auth/register`, 'with data:', { 
        username, 
        email, 
        password: '***', 
        first_name: firstName, 
        last_name: lastName 
      });

      const response = await fetch(`${this.API_BASE_URL}/api/v1/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          email,
          password,
          first_name: firstName,
          last_name: lastName
        }),
      });

      console.log('Registration response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Registration error response:', errorText);
        throw new Error(`Registration failed: ${response.status} - ${errorText}`);
      }

      console.log('Registration successful');
      return true;
    } catch (error) {
      console.error('Registration error:', error);
      // Re-throw with more specific message
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Unable to connect to the server. Please make sure the backend API is running.');
      }
      throw error;
    }
  }

  async logout(): Promise<void> {
    // Remove the token from localStorage
    localStorage.removeItem('access_token');
  }

  isAuthenticated(): boolean {
    const token = localStorage.getItem('access_token');
    return !!token;
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }
}

const authService = new AuthService();
export default authService;