import { NextResponse } from 'next/server';

function isAuthenticated(request) {
  console.log(request.cookies.has('access_token_cookie'))
  return request.cookies.has('access_token_cookie');
}

export function proxy(request) {
  const isAuth = isAuthenticated(request);
  const pathname = request.nextUrl.pathname;

  const protectedRoutes = [
    '/dashboard',
    '/createTimetable',
    '/viewTimetable'
  ];

  const publicOnlyRoutes = [
    '/',       
    '/login'
  ];

  if (protectedRoutes.includes(pathname) && !isAuth) {
    const loginUrl = new URL('/login', request.url);
    return NextResponse.redirect(loginUrl);
  }

  if (publicOnlyRoutes.includes(pathname) && isAuth) {
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
    '/viewTimetable'
  ],
};