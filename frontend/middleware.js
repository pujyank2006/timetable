import { NextResponse } from 'next/server';

export function middleware(request) {
  const token = request.cookies.get('access_token_cookie')?.value;
  const path = request.nextUrl.pathname;

  const protectedRoutes = ['/dashboard', '/createTimetable', '/viewTimetable'];
  const authPage = '/login';

  // 1. Protected route but no token → go to login
  if (protectedRoutes.some(route => path.startsWith(route)) && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // 2. User already logged in and tries to access login → go to dashboard
  if (path.startsWith(authPage) && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  // 3. Home page `/`
  // If logged in → send to dashboard
  if (path === '/' && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    '/',
    '/login',
    '/dashboard',
    '/createTimetable',
    '/viewTimetable',
  ],
};
