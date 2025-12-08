"use client";

import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";

const API_BASE = "http://localhost:5000";

export default function Dashboard() {
    const router = useRouter();
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleLogout() {
        setLoading(true);
        setError("");

        try {
            const response = await fetch(`${API_BASE}/user/logout`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: 'include',
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || "Logout failed");
            }
            router.push("/");
        } catch (err) {
            console.error("Logout Error:", err);
            setError(err.message || "Logout failed");
            alert("Failed to logout: " + err.message);
        } finally {
            setLoading(false);
        }
    }

    const handleReset = async () => {
        try {
            const response = await fetch(`${API_BASE}/availability/reset`, {
                method: 'DELETE',
                credentials: 'include',
            });

            const data = await response.json();

            if (response.ok) {
                console.log('Reset success:', data);
                alert('Availability reset!');
            } else {
                console.log('Reset failed:', data.message);
            }

        } catch (error) {
            console.log('Network error:', error);
        }
    };

    return (
        <>
            <header className="bg-white/80 backdrop-blur sticky top-0 z-20">
                <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
                    <Link href="/dashboard" className="flex items-center gap-3">
                        <img src="/favicon.svg" alt="logo" className="w-8 h-8 rounded-md" />
                        <span className="font-bold text-lg text-slate-800">Timetable</span>
                    </Link>

                    <nav className="flex items-center gap-3">
                        <Link href="/dashboard" className="text-slate-700 hover:text-slate-900 px-3 py-2 rounded-md">Dashboard</Link>
                        <Link href="/createTimetable" className="text-slate-700 hover:text-slate-900 px-3 py-2 rounded-md">Create Timetable</Link>

                        {/* 3. Updated button to show loading state */}
                        <button
                            className="text-slate-700 hover:text-slate-900 px-3 py-2 rounded-md disabled:opacity-50"
                            onClick={handleLogout}
                            disabled={loading}
                        >
                            {loading ? "Logging out..." : "Logout"}
                        </button>
                    </nav>
                </div>
            </header>

            <div className="min-h-screen bg-gray-50 py-8">
                {/* Error Message Display (Optional but helpful) */}
                {error && (
                    <div className="max-w-6xl mx-auto px-4 mb-4">
                        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                            {error}
                        </div>
                    </div>
                )}

                <div className="max-w-6xl mx-auto px-4">
                    <div className="flex items-center justify-between mb-8">
                        <div>
                            <h1 className="text-3xl font-bold text-slate-800">Dashboard</h1>
                            <p className="text-sm text-slate-500">Overview and quick actions</p>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                        <div className="bg-white p-6 rounded-lg shadow-sm">
                            <h2 className="text-lg font-semibold mb-2">Create Timetable</h2>
                            <p className="text-sm text-slate-500 mb-4">Create a new timetable for a class or group.</p>
                            <Link href="/createTimetable">
                                <button className="bg-blue-600 text-white px-4 py-2 rounded-md">Open creator</button>
                            </Link>
                        </div>

                        <div className="bg-white p-6 rounded-lg shadow-sm">
                            <h2 className="text-lg font-semibold mb-2">Recent Timetables</h2>
                            <p className="text-sm text-slate-500 mb-4">View recently generated timetables (placeholder).</p>
                            <Link href="/viewTimetable">
                                <button className="bg-slate-600 text-white px-4 py-2 rounded-md">View</button>
                            </Link>
                        </div>

                        <div className="bg-white p-6 rounded-lg shadow-sm">
                            <h2 className="text-lg font-semibold mb-2">Clear availabilities</h2>
                            <p className="text-sm text-slate-500 mb-4">Clear availabilities for teachers to create new time-tables</p>
                            <button onClick={handleReset} className="bg-red-600 text-white px-4 py-2 rounded-md">Clear</button>
                        </div>
                    </div>

                    <div className="bg-white p-6 rounded-lg shadow-sm">
                        <h3 className="text-base font-semibold mb-3">Activity</h3>
                        <p className="text-sm text-slate-500">No recent activity. Generated timetables and job status will appear here.</p>
                    </div>
                </div>
            </div>
        </>
    );
}