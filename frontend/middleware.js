import { NextResponse } from 'next/server';

export function middleware(request) {
  const token = request.cookies.get('access_token_cookie')?.value;
  const path = request.nextUrl.pathname;

  // Define which are auth-allowed and which are protected
  const publicPaths = ['/login', '/']; 
  const protectedPaths = ['/dashboard', '/createTimetable', '/viewTimetable'];

  // --- RULE 1: BLOCK PROTECTED ROUTES WITHOUT TOKEN ---
  if (protectedPaths.some(route => path.startsWith(route))) {
    if (!token) {
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }

  // --- RULE 2: REDIRECT LOGGED USERS AWAY FROM LOGIN PAGE ---
  if (path.startsWith('/login') && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  // --- RULE 3: IF LOGGED IN AND VISIT ROOT, GO TO DASHBOARD ---
  if (path === '/' && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }
  const response = NextResponse.next();
  response.headers.set("Cache-Control", "no-store, no-cache, must-revalidate");
  return response;
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