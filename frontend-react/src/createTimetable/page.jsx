import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import Header from "../components/Header";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export default function CreateTimetablePage() {
  const [classSelection, setClassSelection] = useState("new");
  const [selectedClass, setSelectedClass] = useState("");
  const [newClassName, setNewClassName] = useState("");
  const [classes, setClasses] = useState([]);
  const [tableRows, setTableRows] = useState([]);

  const handleAddRow = () => {
    setTableRows([
      ...tableRows,
      {
        id: Date.now(),
        teacher_id: "",
        teacher_name: "",
        subject_name: "",
        mobileno: "",
        email: "",
        no_of_classes: "",
        theory_lab: "",
        status: "",
      },
    ]);
  };

  const handleUpdateRow = (id, field, value) => {
    setTableRows(
      tableRows.map((row) => (row.id === id ? { ...row, [field]: value } : row))
    );
  };

  const handleDeleteRow = (id) => {
    setTableRows(tableRows.filter((row) => row.id !== id));
  };

  const handleClear = () => {
    setClassSelection("new");
    setSelectedClass("");
    setNewClassName("");
    setTableRows([]);
    setClasses([]);
  };

  const handleAddToDB = async () => {
    if (classSelection === "new" && !newClassName.trim()) {
      toast.error("Please enter a new class name");
      return;
    }

    try {
      const className = newClassName;
      // Create payload
      const payload = {
        class_name: className,
        teachers: tableRows.map((row) => ({
          id: row.teacher_id,
          name: row.teacher_name,
          subject: [row.subject_name],
          mobileno: row.mobileno,
          email: row.email,
          no_of_classes: parseInt(row.no_of_classes) || 0,
          theory_lab: row.theory_lab,
          status: "pending",
        })),
      };

      const res = await fetch(`${API_BASE}/input/assign`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(errorText || `Server error: ${res.status}`);
      }

      const result = await res.json();
      console.log("Data saved successfully:", result);
      toast.success("Timetable data saved to database successfully!");
      handleClear();
    } catch (err) {
      console.error("Failed to save data:", err);
      toast.error(`Error: ${err.message}`);
    }
  };

  return (
    <>
      <Header />
      <div className="min-h-screen bg-gray-100 py-8">
        <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-9xl mx-auto">
          <h2 className="text-3xl font-semibold mb-6 text-center">Create Timetable</h2>
          {/* Class Selection Section */}
          <div className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <h2 className="text-base font-semibold mb-3">Create Class</h2>
            <div className="flex gap-4 mb-3">
            </div>
            <div className="mb-3">
              <label className="block text-xs font-medium mb-1">Class Name</label>
              <input
                type="text"
                placeholder="Enter new class name (e.g., Class 5)"
                className="w-full p-2 text-sm rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={newClassName}
                onChange={(e) => setNewClassName(e.target.value)}
              />
            </div>
          </div>

          {/* Teacher Table Section */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-4">Teacher Details</h3>
            <div className="overflow-x-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr className="bg-blue-600 text-white">
                    <th className="border border-gray-300 px-4 py-3 text-left">Teacher ID</th>
                    <th className="border border-gray-300 px-4 py-3 text-left">Teacher Name</th>
                    <th className="border border-gray-300 px-4 py-3 text-left">Subject Name</th>
                    <th className="border border-gray-300 px-4 py-3 text-left">Mobile No</th>
                    <th className="border border-gray-300 px-4 py-3 text-left">Email</th>
                    <th className="border border-gray-300 px-4 py-3 text-left">No. of Classes</th>
                    <th className="border border-gray-300 px-4 py-3 text-left">Theory/Lab</th>
                    <th className="border border-gray-300 px-4 py-3 text-center">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {tableRows.length === 0 ? (
                    <tr>
                      <td colSpan="8" className="border border-gray-300 px-4 py-8 text-center text-gray-500">
                        No teacher records added yet. Click "Add Row" to add a new teacher.
                      </td>
                    </tr>
                  ) : (
                    tableRows.map((row) => (
                      <tr key={row.id} className="hover:bg-gray-50">
                        <td className="border border-gray-300 px-4 py-3">
                          <input
                            type="text"
                            className="w-full p-2 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
                            value={row.teacher_id}
                            onChange={(e) =>
                              handleUpdateRow(row.id, "teacher_id", e.target.value)
                            }
                            placeholder="e.g., T001"
                          />
                        </td>
                        <td className="border border-gray-300 px-4 py-3">
                          <input
                            type="text"
                            className="w-full p-2 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
                            value={row.teacher_name}
                            onChange={(e) =>
                              handleUpdateRow(row.id, "teacher_name", e.target.value)
                            }
                            placeholder="e.g., John_Doe"
                          />
                        </td>
                        <td className="border border-gray-300 px-4 py-3">
                          <input
                            type="text"
                            className="w-full p-2 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
                            value={row.subject_name}
                            onChange={(e) =>
                              handleUpdateRow(row.id, "subject_name", e.target.value)
                            }
                            placeholder="Subject"
                          />
                        </td>
                        <td className="border border-gray-300 px-4 py-3">
                          <input
                            type="text"
                            className="w-full p-2 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
                            value={row.mobileno}
                            onChange={(e) =>
                              handleUpdateRow(row.id, "mobileno", e.target.value)
                            }
                            placeholder="Mobile No"
                          />
                        </td>
                        <td className="border border-gray-300 px-4 py-3">
                          <input
                            type="email"
                            className="w-full p-2 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
                            value={row.email}
                            onChange={(e) =>
                              handleUpdateRow(row.id, "email", e.target.value)
                            }
                            placeholder="Email"
                          />
                        </td>
                        <td className="border border-gray-300 px-4 py-3">
                          <input
                            type="number"
                            className="w-full p-2 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
                            value={row.no_of_classes}
                            onChange={(e) =>
                              handleUpdateRow(row.id, "no_of_classes", e.target.value)
                            }
                            placeholder="0"
                            min="0"
                          />
                        </td>
                        <td className="border border-gray-300 px-4 py-3">
                          <input
                            type="text"
                            className="w-full p-2 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
                            value={row.theory_lab}
                            onChange={(e) =>
                              handleUpdateRow(row.id, "theory_lab", e.target.value)
                            }
                            placeholder="Theory/Lab"
                            min="0"
                            step="0.5"
                          />
                        </td>
                        <td className="border border-gray-300 px-4 py-3 text-center">
                          <button
                            onClick={() => handleDeleteRow(row.id)}
                            className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition mr-2"
                          >
                            Delete
                          </button>
                          <button
                            onClick={async () => {
                              if (!row.email) return toast.error("Email is required to send");
                              try {
                                const res = await fetch(`${API_BASE}/api/teachers/generate-link`, {
                                  method: "POST",
                                  headers: {
                                    "Content-Type": "application/json",
                                  },
                                  credentials: "include",
                                  body: JSON.stringify({ teacher_id: row.teacher_id, teacher_email: row.email }),
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
                            className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600 transition mr-2"
                          >
                            Send mail
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
            <button
              onClick={handleAddRow}
              className="mt-4 bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition font-medium"
            >
              + Add Row
            </button>
            <div className="flex gap-4 justify-end mt-3 mb-8">
              <button
                onClick={handleClear}
                className="bg-gray-400 text-white px-6 py-2 rounded-lg hover:bg-gray-500 transition font-medium text-sm"
              >
                Clear
              </button>
              <button
                onClick={handleAddToDB}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition font-medium text-sm"
              >
                Add to DB
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}