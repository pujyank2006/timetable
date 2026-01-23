// src/pages/ViewTimetable.jsx
import { useEffect, useState, useRef } from "react";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
const TIME_SLOTS = ["9:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00", "12:00 - 1:00", "2:00 - 3:00", "3:00 - 4:00", "4:00 - 5:00"];

export default function ViewTimetablePage() {
  const [timetables, setTimetables] = useState([]);
  const [selectedClass, setSelectedClass] = useState("");
  const [currentSchedule, setCurrentSchedule] = useState(null);
  const pdfRef = useRef();

  // 1. Fetch all timetables on load
  useEffect(() => {
    const fetchTimetables = async () => {
      try {
        const res = await fetch(`${API_BASE}/get/time-tables`, {
          credentials: "include",
        });
        if (!res.ok) return;

        const data = await res.json();
        const items = data?.data ?? data ?? [];
        setTimetables(items);

        // Auto-select the first class if available
        if (items.length > 0) {
          setSelectedClass(items[0].class_id);
        }
      } catch (err) {
        console.error("Error fetching timetables:", err);
      }
    };
    fetchTimetables();
  }, []);

  // 2. Update the displayed schedule when selection changes
  useEffect(() => {
    if (!selectedClass || timetables.length === 0) return;

    const found = timetables.find((t) => t.class_id === selectedClass);

    if (found) {
      const slotMap = {};
      const ttable = found.ttable || {};

      Object.entries(ttable).forEach(([subject, slots]) => {
        if (Array.isArray(slots)) {
          slots.forEach((slotIndex) => {
            slotMap[slotIndex] = subject;
          });
        }
      });
      setCurrentSchedule(slotMap);
    } else {
      setCurrentSchedule(null);
    }
  }, [selectedClass, timetables]);

  // Download PDF
  const downloadPDF = () => {
    const doc = new jsPDF("l", "mm", "a4");

    const getSlotContent = (groupName, dayIndex, slotIndex) => {
      const groupData = timetables.find((t) => t.class_id === groupName);
      if (!groupData?.ttable) return "";

      const flatIndex = dayIndex * 7 + slotIndex;

      for (const [subject, slots] of Object.entries(groupData.ttable)) {
        if (slots.includes(flatIndex)) return subject;
      }
      return "";
    };

    let startY = 20;

    doc.setFontSize(18);
    doc.text(`Timetable - ${selectedClass}`, 14, startY);
    startY += 15;

    const DAYS_SHORT = ["Mon", "Tue", "Wed", "Thu", "Fri"];

    const TIME_SLOTS_PDF = [
      "09:00 - 10:00",
      "10:00 - 11:00",
      "11:00 - 12:00",
      "12:00 - 01:00",
      "01:00 - 02:00",
      "02:00 - 03:00",
      "03:00 - 04:00",
    ];

    const tableData = DAYS_SHORT.map((dayName, dayIndex) => {
      const row = [dayName];

      TIME_SLOTS_PDF.forEach((_, slotIndex) => {
        row.push(getSlotContent(selectedClass, dayIndex, slotIndex));
      });

      return row;
    });

    autoTable(doc, {
      startY,
      head: [["Day", ...TIME_SLOTS_PDF]],
      body: tableData,
      theme: "grid",
      styles: { halign: "center" },
      headStyles: { fillColor: [41, 128, 185] },
    });

    doc.save(`Timetable_${selectedClass}.pdf`);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8 flex flex-col items-center">
      {/* Control Bar */}
      <div className="w-full max-w-5xl bg-white p-4 rounded-xl shadow mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Class Timetable</h1>
          <p className="text-sm text-slate-500">Select a class to view schedule</p>
        </div>

        <div className="flex gap-4">
          <select
            className="p-2 border rounded-lg min-w-[200px]"
            value={selectedClass}
            onChange={(e) => setSelectedClass(e.target.value)}
          >
            {timetables.map((t, idx) => {
              const name = t.class_id;
              return (
                <option key={idx} value={name}>
                  {name}
                </option>
              );
            })}
          </select>

          <button
            onClick={downloadPDF}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition"
          >
            <span>Download PDF</span>
          </button>
        </div>
      </div>

      {/* Timetable Display Area */}
      <div
        ref={pdfRef}
        className="w-full max-w-5xl bg-white p-8 rounded-xl shadow-lg border border-gray-200"
      >
        <h2 className="text-center text-3xl font-bold mb-6 text-slate-800 uppercase tracking-wide">
          TIMETABLE: <span className="text-blue-600">{selectedClass}</span>
        </h2>

        <div className="overflow-x-auto">
          <table className="w-full border-collapse border border-gray-300 text-center">
            <thead>
              <tr className="bg-slate-100">
                <th className="p-3 border border-gray-300 font-bold text-slate-700 w-32">
                  Day / Time
                </th>
                {TIME_SLOTS.map((time, i) => (
                  <th
                    key={i}
                    className="p-3 border border-gray-300 font-semibold text-slate-600 text-sm"
                  >
                    {time}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {DAYS.map((day, dayIndex) => (
                <tr key={dayIndex} className="hover:bg-gray-50">
                  <td className="p-3 border border-gray-300 font-bold text-slate-700 bg-slate-50">
                    {day}
                  </td>
                  {TIME_SLOTS.map((_, timeIndex) => {
                    const flatIndex = dayIndex * 7 + timeIndex;
                    const subject = currentSchedule ? currentSchedule[flatIndex] : null;

                    return (
                      <td
                        key={timeIndex}
                        className="p-3 border border-gray-300 h-16 relative group"
                      >
                        {subject ? (
                          <div className="flex flex-col items-center justify-center h-full bg-blue-50/50 rounded-md m-1">
                            <span className="font-bold text-slate-800">{subject}</span>
                          </div>
                        ) : (
                          <span className="text-slate-300 font-bold tracking-widest text-xs">
                            ...
                          </span>
                        )}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}