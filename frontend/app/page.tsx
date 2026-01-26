export default function HomePage() {
  return (
    <div className="home-page">
      {/* Hero Section */}
      <div className="card text-center glass" style={{ background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(236, 72, 153, 0.1))' }}>
        <div className="animate-pulse">
          <h1 className="card-title text-4xl font-extrabold mb-4 bg-gradient-primary bg-clip-text text-transparent">
            Welcome to Smart Todo App
          </h1>
        </div>
        <p className="text-xl text-gray-600 mb-6 leading-relaxed">
          Manage your tasks efficiently with our AI-powered assistant.
        </p>

        <div className="d-flex justify-center gap-4 mt-6 flex-wrap">
          <a href="/auth/login" className="btn btn-primary hover-lift">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: '0.5rem' }}>
              <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
              <polyline points="10 17 15 12 10 7"/>
              <line x1="15" x2="3" y1="12" y2="12"/>
            </svg>
            Login
          </a>
          <a href="/auth/register" className="btn btn-secondary hover-lift">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: '0.5rem' }}>
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
            Register
          </a>
        </div>
      </div>

      {/* Features Section */}
      <div className="card">
        <h2 className="card-title text-3xl font-bold text-center mb-8">Powerful Features</h2>
        <div className="d-grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="d-flex flex-column align-center text-center p-6 rounded-lg border-2 border-gray-100 hover-lift" style={{ transition: 'all 0.3s ease', background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.03), rgba(236, 72, 153, 0.03))' }}>
            <div className="mb-4 p-3 rounded-full bg-gradient-primary text-white animate-bounce" style={{ width: '64px', height: '64px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 2v20M5 5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5Z"/>
              </svg>
            </div>
            <h3 className="text-xl font-bold mb-2 text-gray-800">Advanced Task Management</h3>
            <p className="text-gray-600">Create, update, and manage your tasks efficiently with our intuitive interface.</p>
          </div>

          <div className="d-flex flex-column align-center text-center p-6 rounded-lg border-2 border-gray-100 hover-lift" style={{ transition: 'all 0.3s ease', background: 'linear-gradient(135deg, rgba(6, 182, 212, 0.03), rgba(59, 130, 246, 0.03))' }}>
            <div className="mb-4 p-3 rounded-full bg-gradient-accent text-white animate-bounce" style={{ width: '64px', height: '64px', display: 'flex', alignItems: 'center', justifyContent: 'center', animationDelay: '0.2s' }}>
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 8V4H8"/>
                <circle cx="16" cy="4" r="1"/>
                <path d="M12 2v4h4"/>
                <path d="m22 13-1.23-1.23a1.46 1.46 0 0 0-2.37.39c-.06.23-.09.47-.09.72v1.72a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h12c.25 0 .49.03.72.09a1.46 1.46 0 0 1 .39 2.37L13 13"/>
              </svg>
            </div>
            <h3 className="text-xl font-bold mb-2 text-gray-800">AI-Powered Assistant</h3>
            <p className="text-gray-600">Natural language task management with intelligent suggestions and automation.</p>
          </div>

          <div className="d-flex flex-column align-center text-center p-6 rounded-lg border-2 border-gray-100 hover-lift" style={{ transition: 'all 0.3s ease', background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.03), rgba(34, 197, 94, 0.03))' }}>
            <div className="mb-4 p-3 rounded-full bg-gradient-success text-white animate-bounce" style={{ width: '64px', height: '64px', display: 'flex', alignItems: 'center', justifyContent: 'center', animationDelay: '0.4s' }}>
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect width="20" height="12" x="2" y="6" rx="6" ry="6"/>
                <circle cx="12" cy="12" r="2"/>
              </svg>
            </div>
            <h3 className="text-xl font-bold mb-2 text-gray-800">Enterprise Security</h3>
            <p className="text-gray-600">Protected with industry-standard authentication and end-to-end encryption.</p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="card text-center" style={{ background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(236, 72, 153, 0.05))' }}>
        <h2 className="card-title text-3xl font-bold mb-4">Ready to Transform Your Productivity?</h2>
        <p className="text-xl text-gray-600 mb-6">
          Join thousands of users who are already organizing their lives with Smart Todo App.
        </p>
        <div className="d-flex justify-center gap-4">
          <a href="/auth/register" className="btn btn-primary hover-lift animate-pulse" style={{ maxWidth: '250px' }}>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: '0.5rem' }}>
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
            Start Free Trial
          </a>
          <a href="/tasks" className="btn btn-outline hover-lift">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: '0.5rem' }}>
              <polygon points="12 2 2 7 12 12 22 7 12 2"/>
              <polyline points="2 17 12 22 22 17"/>
              <polyline points="2 12 12 17 22 12"/>
            </svg>
            Try Demo
          </a>
        </div>
      </div>
    </div>
  );
}