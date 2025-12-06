import Link from "next/link";

export default function Home() {
  return (
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
  );
}
