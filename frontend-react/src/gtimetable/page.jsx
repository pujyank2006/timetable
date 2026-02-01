import { useEffect, useState, useRef } from "react";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import Header from "../components/Header";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
const TIME_SLOTS = ["9:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00", "12:00 - 1:00", "2:00 - 3:00", "3:00 - 4:00", "4:00 - 5:00"];

export default function GiantTimetablePage() {
  const [timetables, setTimetables] = useState([]);
  const [selectedClasses, setSelectedClasses] = useState(new Set());
  const [giantSchedule, setGiantSchedule] = useState(null);
  const [loading, setLoading] = useState(false);
  const pdfRef = useRef();

  // Fetch all timetables on load
  useEffect(() => {
    const fetchTimetables = async () => {
      try {
        setLoading(true);
        const res = await fetch(`${API_BASE}/get/time-tables`, {
          credentials: "include",
        });
        if (!res.ok) return;

        const data = await res.json();
        const items = data?.data ?? data ?? [];
        setTimetables(items);
      } catch (err) {
        console.error("Error fetching timetables:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchTimetables();
  }, []);

  // Update giant schedule when selection changes
  useEffect(() => {
    if (selectedClasses.size === 0 || timetables.length === 0) {
      setGiantSchedule(null);
      return;
    }

    const mergedSchedule = {};
    
    selectedClasses.forEach(classId => {
      const timetable = timetables.find(t => t.class_id === classId);
      if (!timetable?.ttable) return;

      Object.entries(timetable.ttable).forEach(([subject, slots]) => {
        if (Array.isArray(slots)) {
          slots.forEach(slotIndex => {
            if (!mergedSchedule[slotIndex]) {
              mergedSchedule[slotIndex] = [];
            }
            mergedSchedule[slotIndex].push({
              class: classId,
              subject: subject
            });
          });
        }
      });
    });

    setGiantSchedule(mergedSchedule);
  }, [selectedClasses, timetables]);

  const handleClassToggle = (classId) => {
    const newSelected = new Set(selectedClasses);
    if (newSelected.has(classId)) {
      newSelected.delete(classId);
    } else {
      newSelected.add(classId);
    }
    setSelectedClasses(newSelected);
  };

  const handleSelectAll = () => {
    if (selectedClasses.size === timetables.length) {
      setSelectedClasses(new Set());
    } else {
      setSelectedClasses(new Set(timetables.map(t => t.class_id)));
    }
  };

  const downloadPDF = () => {
    if (!giantSchedule || selectedClasses.size === 0) return;

    const doc = new jsPDF("l", "mm", "a4");
    let startY = 20;

    doc.setFontSize(18);
    doc.text(`Giant Timetable - ${selectedClasses.size} Classes`, 14, startY);
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
        const flatIndex = dayIndex * 7 + slotIndex;
        const slotData = giantSchedule[flatIndex];
        
        if (slotData && slotData.length > 0) {
          const cellContent = slotData.map(item => `${item.class}: ${item.subject}`).join('\n');
          row.push(cellContent);
        } else {
          row.push("");
        }
      });

      return row;
    });

    autoTable(doc, {
      startY,
      head: [["Day", ...TIME_SLOTS_PDF]],
      body: tableData,
      theme: "grid",
      styles: { halign: "center", fontSize: 8, cellPadding: 2 },
      headStyles: { fillColor: [41, 128, 185] },
      columnStyles: {
        0: { cellWidth: 20 },
        ...Object.fromEntries(Array.from({length: 7}, (_, i) => [i + 1, { cellWidth: 35 }]))
      }
    });

    doc.save(`Giant_Timetable_${selectedClasses.size}_Classes.pdf`);
  };

  const getSlotContent = (dayIndex, timeIndex) => {
    const flatIndex = dayIndex * 7 + timeIndex;
    return giantSchedule?.[flatIndex] || [];
  };

  return (
    <>
      <Header />
      <div className="min-h-screen bg-gray-50 py-8">
        {/* Header and Controls */}
        <div className="w-full max-w-7xl mx-auto">
          <div className="bg-white p-6 rounded-xl shadow mb-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h1 className="text-3xl font-bold text-slate-800 mb-2">Giant Timetable</h1>
                <p className="text-sm text-slate-600">
                  Select multiple classes to create a combined timetable view
                </p>
              </div>
              <div className="flex gap-3">
                <button
                  onClick={handleSelectAll}
                  className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition"
                >
                  {selectedClasses.size === timetables.length ? "Deselect All" : "Select All"}
                </button>
                <button
                  onClick={downloadPDF}
                  disabled={selectedClasses.size === 0}
                  className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg transition flex items-center gap-2"
                >
                  <span>Download PDF</span>
                </button>
              </div>
            </div>

            {/* Class Selection */}
            <div className="border-t pt-4">
              <h3 className="text-lg font-semibold mb-3 text-slate-700">
                Select Classes ({selectedClasses.size} selected)
              </h3>
              {loading ? (
                <div className="text-center py-4 text-slate-500">Loading classes...</div>
              ) : timetables.length === 0 ? (
                <div className="text-center py-4 text-slate-500">
                  No timetables found. Create timetables first.
                </div>
              ) : (
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                  {timetables.map((timetable, idx) => (
                    <label
                      key={idx}
                      className="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-blue-50 transition"
                    >
                      <input
                        type="checkbox"
                        checked={selectedClasses.has(timetable.class_id)}
                        onChange={() => handleClassToggle(timetable.class_id)}
                        className="mr-3 w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                      />
                      <span className="font-medium text-slate-700">
                        {timetable.class_id}
                      </span>
                    </label>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Giant Timetable Display */}
          {selectedClasses.size > 0 && giantSchedule && (
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <h2 className="text-center text-2xl font-bold mb-6 text-slate-800">
                COMBINED TIMETABLE
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
                          className="p-3 border border-gray-300 font-semibold text-slate-600 text-sm min-w-[150px]"
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
                          const slotContent = getSlotContent(dayIndex, timeIndex);

                          return (
                            <td
                              key={timeIndex}
                              className="p-2 border border-gray-300 min-h-[80px] relative"
                            >
                              {slotContent.length > 0 ? (
                                <div className="space-y-1">
                                  {slotContent.map((item, idx) => (
                                    <div
                                      key={idx}
                                      className="bg-blue-50 border border-blue-200 rounded p-1 text-xs"
                                    >
                                      <div className="font-bold text-blue-800">
                                        {item.class}
                                      </div>
                                      <div className="text-slate-700">
                                        {item.subject}
                                      </div>
                                    </div>
                                  ))}
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
          )}
        </div>
      </div>
    </>
  );
}