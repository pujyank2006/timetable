import Link from "next/link";

export default function Home() {
  return (
    <>
      <header className="bg-white/80 backdrop-blur sticky top-0 z-20">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3">
            <img src="/favicon.svg" alt="logo" className="w-8 h-8 rounded-md" />
            <span className="font-bold text-lg text-slate-800">Timetable</span>
          </Link>

          <nav className="flex items-center gap-3">
            <Link href="/login" className="text-slate-700 hover:text-slate-900 px-3 py-2 rounded-md">Login</Link>
          </nav>
        </div>
      </header>
      <div className="min-h-screen bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-white mb-6">Timetable Manager</h1>
          <p className="text-xl text-blue-100 mb-8">Manage your college timetable efficiently</p>

          <Link href="/login">
            <button className="bg-white text-blue-600 font-bold py-3 px-8 rounded-lg hover:bg-blue-50 transition duration-200 text-lg">
              Go to Login
            </button>
          </Link>
        </div>
      </div>
    </>
  );
}
