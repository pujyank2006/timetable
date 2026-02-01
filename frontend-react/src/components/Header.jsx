import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { toast } from "react-toastify";
import { useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export default function Header() {
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

    return (
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
                    <Link
                        to="/viewTimetable"
                        className="text-slate-700 hover:text-slate-900 px-3 py-2 rounded-md"
                    >
                        View Timetable
                    </Link>
                    <Link
                        to="/gtimetable"
                        className="text-slate-700 hover:text-slate-900 px-3 py-2 rounded-md"
                    >
                        Giant Timetable
                    </Link>
                    <Link
                        to="/responses"
                        className="text-slate-700 hover:text-slate-900 px-3 py-2 rounded-md"
                    >
                        Responses
                    </Link>
                    <Link
                        to="/invigilation"
                        className="text-slate-700 hover:text-slate-900 px-3 py-2 rounded-md"
                    >
                        Invigilation
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
    );
}
