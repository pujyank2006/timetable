import React, { useState, useEffect } from 'react';
import { toast } from "react-toastify";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export default function ResponsesPage() {
    const [inputData, setInputData] = useState([]);
    const [classes, setClasses] = useState([]);
    const [selectedClass, setSelectedClass] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [selectedTeacherForModal, setSelectedTeacherForModal] = useState(null);
    const [availabilityMap, setAvailabilityMap] = useState(null);
    const [avaSlots, setAvaSlots] = useState({});

    useEffect(() => {
        const fetchInputData = async () => {
            try {
                setLoading(true);
                const response = await fetch(`${API_BASE}/input/input-data`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    credentials: "include",
                });

                if (!response.ok) {
                    throw new Error(`Failed to fetch data: ${response.status}`);
                }

                const result = await response.json();
                if (result.success) {
                    setInputData(result.data);
                    setClasses(result.classes);
                    if (result.classes.length > 0) {
                        setSelectedClass(result.classes[0]);
                    }
                } else {
                    setError(result.error || "Failed to fetch data");
                }
            } catch (err) {
                console.error("Error fetching input data:", err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        const fetchAvailability = async () => {
            try {
                const res = await fetch(`${API_BASE}/availability/all`, {
                    credentials: "include",
                });
                if (!res.ok) return;
                const data = await res.json();
                const map = {};
                (data || []).forEach((rec) => {
                    const key = rec.teacher_id;
                    if (key) {
                        map[key] = rec;
                    }
                });
                setAvailabilityMap(map);
            } catch (err) {
                console.error("Error fetching availability:", err);
            }
        };

        fetchInputData();
        fetchAvailability();
    }, []);

    // Filter teachers based on selected class
    const getTeachersForClass = () => {
        const classData = inputData.find(item => item.class_name === selectedClass);
        return classData ? classData.teachers : [];
    };

    const handleSeeResponse = async (teacher) => {
        try {
            // Show the modal immediately with a loading state
            setSelectedTeacherForModal({ ...teacher, loadingResponse: true });
            console.log("Fetching response for teacher ID:", teacher.id);
            const response = await fetch(`${API_BASE}/availability/response/${teacher.id}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
            });

            if (response.ok) {
                const result = await response.json();
                // Update the state with the availability data
                setSelectedTeacherForModal({
                    ...teacher,
                    availabilityData: result,
                    loadingResponse: false
                });
            } else {
                // If no data found, just close the loading state
                setSelectedTeacherForModal({
                    ...teacher,
                    availabilityData: null,
                    loadingResponse: false
                });
            }
        } catch (err) {
            console.error("Failed to fetch teacher response:", err);
            setSelectedTeacherForModal({
                ...teacher,
                availabilityData: null,
                loadingResponse: false,
                error: err.message
            });
        }
    };


    const handleGenerate = async () => {
        const found = inputData?.find(
            data => data?.class_name === selectedClass
        );
        const cls = found?.["class_name"]
        const teacher = found?.["teachers"]

        // Student groups
        const studentgroups = [
            {
                group: cls,
                subjects: teacher.reduce((acc, row) => {
                    row.subject?.forEach(subject => {
                        acc[subject] =
                            (acc[subject] || 0) + (parseInt(row.no_of_classes) || 0);
                    });
                    return acc;
                }, {}),
            },
        ];

        // teachers
        const teachers = teacher.map((row) => ({
            name: row.name,
            subject: row.subject,
        }))

        // un-availability
        const teacherunavailability = teacher.map((row) => ({
            name: row.name,
            slots: avaSlots[row.id] || []
        }))

        const finalPayload = {
            studentgroups,
            teachers,
            teacherunavailability,
        };

        const json_input = finalPayload;
        console.log(json_input);
        try {
            const res = await fetch(`${API_BASE}/generate/time-table`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
                body: JSON.stringify(json_input),
            });

            if (!res.ok) {
                const errorText = await res.text();
                throw new Error(errorText || `Server error: ${res.status}`);
            }

            const result = await res.json();
            console.log("Timetable generated successfully:", result);
            toast.success("Timetable generation started successfully!");
        } catch (err) {
            console.error("Failed to submit timetable configuration:", err);
            toast.error(`Error submitting data: ${err.message}`);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-100 p-6 flex items-center justify-center">
                <div className="text-xl font-semibold text-gray-700">Loading...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gray-100 p-6 flex items-center justify-center">
                <div className="text-xl font-semibold text-red-600">Error: {error}</div>
            </div>
        );
    }

    const teachers = getTeachersForClass();

    return (
        <div className="min-h-screen bg-gray-100 p-6">
            <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-6xl mx-auto">
                <h2 className="text-3xl font-semibold mb-6 text-center">Response Details</h2>

                {/* Class Selection Dropdown */}
                <div className="mb-8 p-4 bg-gray-50 rounded-lg border border-gray-200">
                    <label className="block text-base font-semibold mb-3 text-gray-700">
                        Select Class:
                    </label>
                    <select
                        value={selectedClass}
                        onChange={(e) => setSelectedClass(e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
                    >
                        {classes.map((className, index) => (
                            <option key={index} value={className}>
                                {className}
                            </option>
                        ))}
                    </select>
                </div>

                {/* Teachers Table */}
                <div className="mt-8">
                    <h3 className="text-2xl font-semibold mb-4 text-gray-700">
                        Teachers for {selectedClass}
                    </h3>

                    {teachers.length === 0 ? (
                        <div className="text-center py-8 text-gray-500">
                            No teachers found for this class.
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full border-collapse">
                                <thead>
                                    <tr className="bg-blue-500 text-white">
                                        <th className="border border-gray-300 px-4 py-3 text-left font-semibold">
                                            ID
                                        </th>
                                        <th className="border border-gray-300 px-4 py-3 text-left font-semibold">
                                            Name
                                        </th>
                                        <th className="border border-gray-300 px-4 py-3 text-left font-semibold">
                                            Email
                                        </th>
                                        <th className="border border-gray-300 px-4 py-3 text-left font-semibold">
                                            No. of Classes
                                        </th>
                                        <th className="border border-gray-300 px-4 py-3 text-left font-semibold">
                                            Theory/Lab
                                        </th>
                                        <th className="border border-gray-300 px-4 py-3 text-center font-semibold">
                                            Action
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {teachers.map((teacher, index) => (
                                        <tr
                                            key={index}
                                            className="hover:bg-gray-50 border-b border-gray-200"
                                        >
                                            <td className="border border-gray-300 px-4 py-3 text-gray-700">
                                                {teacher.id}
                                            </td>
                                            <td className="border border-gray-300 px-4 py-3 text-gray-700">
                                                {teacher.name}
                                            </td>
                                            <td className="border border-gray-300 px-4 py-3 text-gray-700">
                                                {teacher.email}
                                            </td>
                                            <td className="border border-gray-300 px-4 py-3 text-gray-700 text-center">
                                                {teacher.no_of_classes}
                                            </td>
                                            <td className="border border-gray-300 px-4 py-3 text-gray-700 text-center">
                                                {teacher.theory_lab}
                                            </td>
                                            <td className="border border-gray-300 px-4 py-3 text-center">
                                                <button
                                                    onClick={() => handleSeeResponse(teacher)}
                                                    className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors font-medium"
                                                >
                                                    See Response
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
                <div className="flex justify-end mt-4">
                    <button
                        onClick={handleGenerate}
                        className="px-6 py-2 bg-orange-600 text-white rounded-lg hover:bg-green-600 transition-colors font-medium"
                    >
                        Generate
                    </button>
                </div>

            </div>
            {/* Modal Overlay */}
            {selectedTeacherForModal && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-white/30 backdrop-blur-md">
                    {/* Modal Container */}
                    <div className="bg-white rounded-2xl shadow-2xl w-full max-w-4xl max-h-[80vh] overflow-y-auto animate-in fade-in zoom-in duration-200">
                        {/* Modal Header */}
                        <div className="bg-blue-500 p-4 flex justify-between items-center text-white">
                            <h3 className="text-xl font-bold">Teacher Submitted Availability</h3>
                            <button
                                onClick={() => setSelectedTeacherForModal(null)}
                                className="hover:bg-blue-600 rounded-full p-1 transition-colors"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                        </div>

                        {/* Modal Body */}
                        <div className="p-6 space-y-6">
                            {selectedTeacherForModal.loadingResponse ? (
                                <div className="text-center py-8">
                                    <p className="text-gray-500">Loading availability data...</p>
                                </div>
                            ) : (
                                <>
                                    {/* Availability Data Section */}
                                    {selectedTeacherForModal.availabilityData ? (
                                        <div>
                                            {/* Submitted Status */}
                                            <div className="mb-6">
                                                <p className="text-sm text-gray-500 uppercase font-bold mb-2">
                                                    Status
                                                </p>
                                                {selectedTeacherForModal.availabilityData.submitted ? (
                                                    <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-semibold bg-green-100 text-green-700">
                                                        ✓ Submitted
                                                    </span>
                                                ) : (
                                                    <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-semibold bg-yellow-100 text-yellow-700">
                                                        ⊘ Pending
                                                    </span>
                                                )}
                                            </div>

                                            {/* Availability Grid */}
                                            <div className="space-y-4">
                                                {(() => {
                                                    const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
                                                    const hours = ["9-10", "10-11", "11-12", "12-1", "2-3", "3-4", "4-5"];

                                                    const grid = {};
                                                    days.forEach(day => {
                                                        grid[day] = new Array(hours.length).fill(0);
                                                    });

                                                    const unavailable =
                                                        selectedTeacherForModal.availabilityData.authentic_unavailability || [];

                                                    unavailable.forEach(index => {
                                                        const dayIndex = Math.floor(index / hours.length);
                                                        const hourIndex = index % hours.length;
                                                        if (days[dayIndex]) {
                                                            grid[days[dayIndex]][hourIndex] = 1;
                                                        }
                                                    });


                                                    return days.map(day => (
                                                        <div key={day}>
                                                            <p className="font-semibold text-gray-700 mb-2 text-sm">{day}</p>
                                                            <div className="flex flex-wrap gap-2">
                                                                {hours.map((hr, idx) => (
                                                                    <div
                                                                        key={idx}
                                                                        className={`px-3 py-1 rounded-md text-xs font-medium border text-center min-w-[60px 
                                                                                ${grid[day][idx] === 1
                                                                                ? "bg-red-500 text-white border-red-500"
                                                                                : "bg-green-100 text-green-800 border-green-300"
                                                                            }`}
                                                                    >
                                                                        {hr}
                                                                    </div>
                                                                ))}
                                                            </div>
                                                        </div>
                                                    ));
                                                })()}
                                            </div>

                                            {/* Legend */}
                                            <div className="mt-5 flex gap-4 text-sm">
                                                <div className="flex items-center gap-2">
                                                    <span className="w-3 h-3 bg-red-500 rounded"></span>
                                                    <span className="text-gray-600">Not Available</span>
                                                </div>
                                                <div className="flex items-center gap-2">
                                                    <span className="w-3 h-3 bg-green-100 border border-green-300 rounded"></span>
                                                    <span className="text-gray-600">Available</span>
                                                </div>
                                            </div>
                                        </div>
                                    ) : (
                                        <div className="text-center py-8">
                                            <p className="text-gray-500">No availability data found for this teacher</p>
                                        </div>
                                    )}

                                    {/* Close Button */}
                                    <div className="pt-4 border-t border-gray-200 flex gap-4"> {/* Added 'flex' and 'gap-4' */}
                                        <button
                                            onClick={() => {
                                                const slots = availabilityMap[selectedTeacherForModal.id]?.authentic_unavailability;
                                                console.log(slots);
                                                setAvaSlots(prev => ({
                                                    ...prev,
                                                    [selectedTeacherForModal.id]: slots ?? []
                                                }));
                                            }}
                                            className="flex-1 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors font-semibold text-sm"
                                        >
                                            Accept
                                        </button>
                                        <button
                                            onClick={async () => {
                                                if (!selectedTeacherForModal.email) return toast.error("Email is required to send");
                                                try {
                                                    const res = await fetch(`${API_BASE}/api/teachers/generate-link`, {
                                                        method: "POST",
                                                        headers: {
                                                            "Content-Type": "application/json",
                                                        },
                                                        credentials: "include",
                                                        body: JSON.stringify({ teacher_id: selectedTeacherForModal.id, teacher_email: selectedTeacherForModal.email }),
                                                    });

                                                    if (!res.ok) {
                                                        const text = await res.text();
                                                        toast.error(text || "Failed to send email");
                                                    } else {
                                                        toast.success("Email sent successfully");
                                                    }
                                                } catch (err) {
                                                    console.error(err);
                                                    toast.error("Error sending email");
                                                }
                                            }}
                                            className="flex-1 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors font-semibold text-sm"
                                        >
                                            Reject
                                        </button>
                                    </div>
                                </>
                            )}
                        </div>
                    </div>
                </div>
            )
            }
        </div >
    );
}