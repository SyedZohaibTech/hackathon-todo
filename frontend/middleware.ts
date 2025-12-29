import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  // Get the auth token from cookies
  const authToken = request.cookies.get('better-auth.session_token');
  const isAuthenticated = !!authToken;

  // Define protected routes that require authentication
  const protectedRoutes = ['/', '/dashboard'];
  // Define public routes that should redirect if user is authenticated
  const publicRoutes = ['/login', '/signup'];

  const currentPath = request.nextUrl.pathname;

  // If user is not authenticated and trying to access protected routes
  if (!isAuthenticated && protectedRoutes.some(route => currentPath.startsWith(route))) {
    // Redirect to login page
    const url = request.nextUrl.clone();
    url.pathname = '/login';
    url.search = `?redirect=${encodeURIComponent(request.url)}`;
    return NextResponse.redirect(url);
  }

  // If user is authenticated and trying to access public routes (login/signup)
  if (isAuthenticated && publicRoutes.some(route => currentPath.startsWith(route))) {
    // Redirect to dashboard/home
    const url = request.nextUrl.clone();
    url.pathname = '/';
    return NextResponse.redirect(url);
  }

  return NextResponse.next();
}

// Configure which paths the middleware should run for
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    // Updated to exclude more static resources that don't need auth checks
    '/((?!api|_next/static|_next/image|favicon.ico|assets|images|fonts|svg|png|jpg|jpeg|gif|webp|css|js).*)',
  ],
};