import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { toast } from "react-toastify";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export default function Dashboard() {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const { logout } = useAuth();

    async function handleLogout() {
        setLoading(true);

        try {
            const response = await fetch(`${API_BASE}/user/logout`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || "Logout failed");
            }
            logout();
            navigate("/");
        } catch (err) {
            console.error("Logout Error:", err);
            toast.error("Failed to logout: " + err.message);
        } finally {
            setLoading(false);
        }
    }

    const handleReset = async () => {
        try {
            const response = await fetch(`${API_BASE}/availability/reset`, {
                method: "DELETE",
                credentials: "include",
            });

            const data = await response.json();

            if (response.ok) {
                console.log("Reset success:", data);
                toast.success("Availability reset!");
            } else {
                console.log("Reset failed:", data.message);
                toast.error(data.message || "Reset failed");
            }
        } catch (error) {
            console.log("Network error:", error);
            toast.error("Network error: " + error.message);
        }
    };

    return (
        <>
            <header className="bg-white/80 backdrop-blur sticky top-0 z-20">
                <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
                    <Link to="/dashboard" className="flex items-center gap-3">
                        <img src="/favicon.svg" alt="logo" className="w-8 h-8 rounded-md" />
                        <span className="font-bold text-lg text-slate-800">Timetable</span>
                    </Link>

                    <nav className="flex items-center gap-3">
                        <Link
                            to="/dashboard"
                            className="text-slate-700 hover:text-slate-900 px-3 py-2 rounded-md"
                        >
                            Dashboard
                        </Link>
                        <Link
                            to="/createTimetable"
                            className="text-slate-700 hover:text-slate-900 px-3 py-2 rounded-md"
                        >
                            Create Timetable
                        </Link>

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
                <div className="max-w-6xl mx-auto px-4">
                    <div className="flex items-center justify-between mb-8">
                        <div>
                            <h1 className="text-3xl font-bold text-slate-800">Dashboard</h1>
                            <p className="text-sm text-slate-500">Overview and quick actions</p>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                        <div className="bg-white p-6 rounded-lg shadow-sm">
                            <h2 className="text-lg font-semibold mb-2">Create Timetable</h2>
                            <p className="text-sm text-slate-500 mb-4">
                                Create a new timetable for a class or group.
                            </p>
                            <Link to="/createTimetable">
                                <button className="bg-blue-600 text-white px-4 py-2 rounded-md">
                                    Open creator
                                </button>
                            </Link>
                        </div>

                        <div className="bg-white p-6 rounded-lg shadow-sm">
                            <h2 className="text-lg font-semibold mb-2">Recent Timetables</h2>
                            <p className="text-sm text-slate-500 mb-4">
                                View recently generated timetables (placeholder).
                            </p>
                            <Link to="/viewTimetable">
                                <button className="bg-slate-600 text-white px-4 py-2 rounded-md">
                                    View
                                </button>
                            </Link>
                        </div>

                        <div className="bg-white p-6 rounded-lg shadow-sm">
                            <h2 className="text-lg font-semibold mb-2">Availabilities</h2>
                            <p className="text-sm text-slate-500 mb-4">
                                View the responses of teachers to availability requests and approve them to create timetables.
                            </p>
                            <Link to="/responses">
                                <button className="bg-green-600 text-white px-4 py-2 rounded-md">
                                    Check Responses
                                </button>
                            </Link>
                        </div>

                        <div className="bg-white p-6 rounded-lg shadow-sm">
                            <h2 className="text-lg font-semibold mb-2">Assign Invigilators</h2>
                            <p className="text-sm text-slate-500 mb-4">
                                Assign teachers to invigilate upcoming exams
                            </p>
                            <Link to="/invigilation">
                                <button className="bg-yellow-600 text-white px-4 py-2 rounded-md">
                                    Assign
                                </button>
                            </Link>
                        </div>

                        <div className="bg-white p-6 rounded-lg shadow-sm">
                            <h2 className="text-lg font-semibold mb-2">Clear availabilities</h2>
                            <p className="text-sm text-slate-500 mb-4">
                                Clear availabilities for teachers to create new timetables
                            </p>
                            <button
                                onClick={handleReset}
                                className="bg-red-600 text-white px-4 py-2 rounded-md"
                            >
                                Clear
                            </button>
                        </div>

                        <div className="bg-white p-6 rounded-lg shadow-sm">
                            <h2 className="text-lg font-semibold mb-2">Click for department timetable</h2>
                            <p className="text-sm text-slate-500 mb-4">
                                Select the classes of your department to get giant timetable
                            </p>
                            <Link
                                to="/gtimetable"
                                className="bg-purple-600 text-white px-4 py-2 rounded-md inline-block text-center"
                            >
                                Department timetable
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}
