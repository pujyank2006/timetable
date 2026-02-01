import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { toast } from "react-toastify";
import Header from "../components/Header.jsx";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export default function InvigulationPage() {
    const navigate = useNavigate();
    const { logout } = useAuth();

    const [teacherInput, setTeacherInput] = useState("");
    const [formData, setFormData] = useState({
        exam_date_from: "",
        exam_date_to: "",
        teachers_per_day: 2,
        exam_time_start: "09:00",
        exam_time_end: "12:00"
    });

    const [assignments, setAssignments] = useState(null);
    const [loading, setLoading] = useState(false);

    const parseTeachers = () => {
        return teacherInput
            .split('\n')
            .map(name => name.trim())
            .filter(name => name.length > 0);
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: name === "teachers_per_day" ? parseInt(value) : value
        }));
    };

    const handleAssignInvigilators = async (e) => {
        e.preventDefault();

        const selectedTeachers = parseTeachers();

        // Validation
        if (!formData.exam_date_from || !formData.exam_date_to) {
            toast.error("Please select both start and end dates");
            return;
        }

        if (new Date(formData.exam_date_from) > new Date(formData.exam_date_to)) {
            toast.error("End date must be after start date");
            return;
        }

        if (selectedTeachers.length === 0) {
            toast.error("Please enter at least one teacher name");
            return;
        }

        if (formData.teachers_per_day <= 0) {
            toast.error("Teachers per day must be greater than 0");
            return;
        }

        if (!formData.exam_time_start || !formData.exam_time_end) {
            toast.error("Please select exam times");
            return;
        }

        if (formData.exam_time_start >= formData.exam_time_end) {
            toast.error("End time must be after start time");
            return;
        }

        try {
            setLoading(true);
            const response = await fetch(`${API_BASE}/invigilators/assign`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
                body: JSON.stringify({
                    exam_date_from: formData.exam_date_from,
                    exam_date_to: formData.exam_date_to,
                    teacher_names: selectedTeachers,
                    teachers_per_day: formData.teachers_per_day,
                    exam_time_start: formData.exam_time_start,
                    exam_time_end: formData.exam_time_end
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || "Failed to assign invigilators");
            }

            const data = await response.json();
            if (data.success) {
                setAssignments(data.assignments);
                toast.success("Invigilators assigned successfully!");
            }
        } catch (err) {
            console.error("Error:", err);
            toast.error(err.message || "Failed to assign invigilators");
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = async () => {
        try {
            await fetch(`${API_BASE}/user/logout`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
            });
            logout();
            navigate("/");
        } catch (err) {
            console.error("Logout Error:", err);
        }
    };

    const calculateDays = () => {
        if (!formData.exam_date_from || !formData.exam_date_to) return 0;
        const from = new Date(formData.exam_date_from);
        const to = new Date(formData.exam_date_to);
        return Math.ceil((to - from) / (1000 * 60 * 60 * 24)) + 1;
    };

    return (
        <>
            <Header />
            <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-4xl mx-auto px-4">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-slate-800">Assign Invigilators</h1>
                    <p className="text-sm text-slate-500 mt-1">
                        Automatically assign teachers to invigilate exams
                    </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Form Section */}
                    <div className="lg:col-span-2">
                        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
                            <form onSubmit={handleAssignInvigilators} className="space-y-6">
                                {/* Date Range Section */}
                                <div>
                                    <h3 className="text-lg font-semibold text-slate-800 mb-4">
                                        Exam Period
                                    </h3>
                                    <div className="grid grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-sm font-medium text-slate-700 mb-1">
                                                Start Date
                                            </label>
                                            <input
                                                type="date"
                                                name="exam_date_from"
                                                value={formData.exam_date_from}
                                                onChange={handleInputChange}
                                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                                required
                                            />
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-slate-700 mb-1">
                                                End Date
                                            </label>
                                            <input
                                                type="date"
                                                name="exam_date_to"
                                                value={formData.exam_date_to}
                                                onChange={handleInputChange}
                                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                                required
                                            />
                                        </div>
                                    </div>
                                    {calculateDays() > 0 && (
                                        <p className="text-xs text-slate-500 mt-2">
                                            Total days: {calculateDays()}
                                        </p>
                                    )}
                                </div>

                                {/* Time Section */}
                                <div>
                                    <h3 className="text-lg font-semibold text-slate-800 mb-4">
                                        Exam Time
                                    </h3>
                                    <div className="grid grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-sm font-medium text-slate-700 mb-1">
                                                Start Time
                                            </label>
                                            <input
                                                type="time"
                                                name="exam_time_start"
                                                value={formData.exam_time_start}
                                                onChange={handleInputChange}
                                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                                required
                                            />
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-slate-700 mb-1">
                                                End Time
                                            </label>
                                            <input
                                                type="time"
                                                name="exam_time_end"
                                                value={formData.exam_time_end}
                                                onChange={handleInputChange}
                                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                                required
                                            />
                                        </div>
                                    </div>
                                </div>

                                {/* Teachers Per Day */}
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-2">
                                        Teachers Required Per Day
                                    </label>
                                    <input
                                        type="number"
                                        name="teachers_per_day"
                                        min="1"
                                        value={formData.teachers_per_day}
                                        onChange={handleInputChange}
                                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                        required
                                    />
                                    <p className="text-xs text-slate-500 mt-1">
                                        {calculateDays() > 0 && (
                                            <>
                                                Total teachers needed: {calculateDays() * formData.teachers_per_day} slot(s)
                                            </>
                                        )}
                                    </p>
                                </div>

                                {/* Submit Button */}
                                <button
                                    type="submit"
                                    disabled={loading}
                                    className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-md transition-colors"
                                >
                                    {loading ? "Assigning..." : "Assign Invigilators"}
                                </button>
                            </form>
                        </div>
                    </div>

                    {/* Teachers Input Sidebar */}
                    <div className="lg:col-span-1">
                        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200 sticky top-20">
                            <h3 className="text-lg font-semibold text-slate-800 mb-4">
                                Teacher Names
                            </h3>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-2">
                                    Enter teacher names (one per line)
                                </label>
                                <textarea
                                    value={teacherInput}
                                    onChange={(e) => setTeacherInput(e.target.value)}
                                    placeholder="John Doe&#10;Jane Smith&#10;Robert Johnson&#10;..."
                                    className="w-full h-64 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm resize-none"
                                />
                                <div className="mt-4 pt-4 border-t border-gray-200">
                                    <p className="text-sm font-medium text-slate-700">
                                        Teachers to assign: <span className="text-blue-600">{parseTeachers().length}</span>
                                    </p>
                                    {parseTeachers().length > 0 && (
                                        <div className="mt-3 space-y-1">
                                            {parseTeachers().map((teacher, idx) => (
                                                <div key={idx} className="text-xs text-slate-600 bg-gray-50 px-2 py-1 rounded">
                                                    {idx + 1}. {teacher}
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Results Section */}
                {assignments && (
                    <div className="mt-8">
                        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
                            <div className="flex items-center justify-between mb-6">
                                <h2 className="text-2xl font-bold text-slate-800">
                                    Invigilator Assignments
                                </h2>
                                <button
                                    onClick={() => window.print()}
                                    className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md text-sm transition-colors"
                                >
                                    Print
                                </button>
                            </div>

                            <div className="space-y-4">
                                {assignments.map((dayAssignment, index) => (
                                    <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                                        <div className="flex items-center justify-between mb-3">
                                            <h3 className="text-lg font-semibold text-slate-800">
                                                {new Date(dayAssignment.date).toLocaleDateString('en-US', {
                                                    weekday: 'long',
                                                    year: 'numeric',
                                                    month: 'long',
                                                    day: 'numeric'
                                                })}
                                            </h3>
                                            <span className="bg-blue-100 text-blue-800 text-sm font-medium px-3 py-1 rounded-full">
                                                {dayAssignment.teachers.length} teacher(s)
                                            </span>
                                        </div>
                                        <div className="flex flex-wrap gap-2">
                                            {dayAssignment.teachers.map((teacher, tIndex) => (
                                                <div
                                                    key={tIndex}
                                                    className="bg-gray-50 border border-gray-300 text-slate-700 px-3 py-2 rounded-md text-sm"
                                                >
                                                    {teacher}
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>

                            <div className="mt-6 pt-6 border-t border-gray-200">
                                <div className="grid grid-cols-3 gap-4">
                                    <div className="bg-blue-50 p-4 rounded-lg">
                                        <p className="text-sm text-slate-600">Total Days</p>
                                        <p className="text-2xl font-bold text-blue-600">
                                            {assignments.length}
                                        </p>
                                    </div>
                                    <div className="bg-green-50 p-4 rounded-lg">
                                        <p className="text-sm text-slate-600">Total Assignments</p>
                                        <p className="text-2xl font-bold text-green-600">
                                            {assignments.reduce((sum, day) => sum + day.teachers.length, 0)}
                                        </p>
                                    </div>
                                    <div className="bg-purple-50 p-4 rounded-lg">
                                        <p className="text-sm text-slate-600">Unique Teachers</p>
                                        <p className="text-2xl font-bold text-purple-600">
                                            {new Set(assignments.flatMap(d => d.teachers)).size}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    </>
  );
}
