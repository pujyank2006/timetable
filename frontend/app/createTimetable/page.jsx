"use client";
import { useEffect, useState } from "react";
const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;

export default function CreateTimetablePage() {
  const [classes, setClasses] = useState([]);
  const [selectedClass, setSelectedClass] = useState("");
  const [teachers, setTeachers] = useState([]);
  const [availabilityMap, setAvailabilityMap] = useState({});
  const [slots, setSlots] = useState([]);


  useEffect(() => {
    const fetchClasses = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/classes`, {
          credentials: 'include'
        });

        if (!res.ok) {
          console.error("Failed to fetch classes", res.statusText);
          return;
        }

        const data = await res.json();
        const items = data?.data ?? data ?? [];
        setClasses(items);
        if (items.length > 0) setSelectedClass(getDisplayName(items[0]));
      } catch (err) {
        console.error("Error fetching classes:", err);
      }
    };

    const fetchTeachers = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/teachers`, {
          credentials: 'include'
        });
        if (!res.ok) return;
        const data = await res.json();
        const items = data?.data ?? data ?? [];
        setTeachers(items);
      } catch (err) {
        console.error("Error fetching teachers:", err);
      }
    };

    const fetchAvailability = async () => {
      try {
        const res = await fetch(`${API_BASE}/availability/all`, {
          credentials: 'include'
        });
        if (!res.ok) return;
        const data = await res.json();
        const map = {};
        (data || []).forEach((rec) => {
          const key = String(rec.teacher_id ?? rec.id ?? rec.name ?? rec._id ?? "");
          map[key] = rec;
        });
        setAvailabilityMap(map);
      } catch (err) {
        console.error("Error fetching availability:", err);
      }
    };

    fetchClasses();
    fetchTeachers();
    fetchAvailability();
  }, []);

  function getDisplayName(c) {
    if (!c) return "";
    return c.name ?? c.class ?? c.class_id ?? c.id ?? (typeof c === "string" ? c : JSON.stringify(c));
  }

  function getSubjectsForSelected() {
    if (!selectedClass || classes.length === 0) return [];
    const cls = classes.find((c) => getDisplayName(c) === selectedClass);
    if (!cls) return [];

    const subjectsField = cls.subjects ?? cls.subject_list ?? cls.subjects_list ?? cls.subjectsMap ?? cls.subjectMap ?? cls.subjectsObj;
    if (!subjectsField) {
      if (Array.isArray(cls.subject)) return cls.subject;
      if (typeof cls.subject === "string") return cls.subject.split(/,\s*/).filter(Boolean);
      return [];
    }

    if (Array.isArray(subjectsField)) return subjectsField;
    if (typeof subjectsField === "object") return Object.keys(subjectsField);
    if (typeof subjectsField === "string") return subjectsField.split(/,\s*/).filter(Boolean);
    return [];
  }

  // initialize slots to match subjects when class changes
  useEffect(() => {
    const subs = getSubjectsForSelected();
    if (!subs || subs.length === 0) {
      setSlots([]);
      return;
    }
    setSlots(subs.map((s) => ({ subject: s, teacherId: "", count: "" })));
  }, [selectedClass, classes, teachers]);

  function getTeachersForSubject(subject) {
    if (!subject) return [];
    if (!teachers || teachers.length === 0) return [];

    return teachers.filter((t) => {
      const subjField = t.subject ?? t.subjects ?? t.teaches ?? null;
      if (!subjField) return false;
      if (Array.isArray(subjField)) return subjField.some((s) => String(s).toLowerCase() === String(subject).toLowerCase());
      return String(subjField).toLowerCase() === String(subject).toLowerCase();
    });
  }

  function getTeacherId(t) {
    return String(t.id ?? t._id ?? t.teacher_id ?? t.email ?? t.name ?? "");
  }

  function generateTimetableJSON() {
    const selectedTeacherIds = new Set(
      slots.map(s => s.teacherId).filter(id => id && id !== "")
    );

    const subjectsMap = {};
    slots.forEach((slot) => {
      subjectsMap[slot.subject] = Number(slot.count) || 0;
    });

    const studentGroups = [
      {
        group: selectedClass,
        subjects: subjectsMap,
      },
    ];

    const filteredTeachers = teachers.filter(t => selectedTeacherIds.has(getTeacherId(t)));

    const teachersList = filteredTeachers.map((t) => {
      const subjRaw = t.subject ?? t.subjects ?? t.teaches ?? "";
      const subjStr = Array.isArray(subjRaw) ? subjRaw.join(", ") : String(subjRaw);

      return {
        name: t.name ?? t.fullname ?? t.id ?? "Unknown",
        subject: subjStr,
      };
    });

    const teacherUnavailability = Object.values(availabilityMap)
      .filter(rec => selectedTeacherIds.has(String(rec.teacher_id)))
      .map((rec) => {
        const tObj = teachers.find((t) => String(t.id) === String(rec.teacher_id));
        const tName = tObj ? (tObj.name ?? tObj.fullname) : (rec.name ?? rec.teacher_id);

        return {
          name: tName,
          slots: rec.slots ?? rec.unavailable_slots ?? [],
        };
      });

    const payload = {
      studentgroups: studentGroups,
      teachers: teachersList,
      teacherunavailability: teacherUnavailability,
    };

    console.log("Generated JSON:", JSON.stringify(payload, null, 2));
    // alert("JSON generated! Check the console.");
    return payload;
  }

  const submitTimetableData = async (payload) => {
    try {
      const res = await fetch(`${API_BASE}/generate/time-table`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: 'include',
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(errorText || `Server error: ${res.status}`);
      }

      const result = await res.json();
      console.log("Timetable generated successfully:", result);
      alert("Timetable generation started successfully!");

    } catch (err) {
      console.error("Failed to submit timetable configuration:", err);
      alert(`Error submitting data: ${err.message}`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex justify-center items-center p-6">
      <div className="bg-white shadow-xl rounded-2xl p-6 w-full max-w-md">
        <h2 className="text-2xl font-semibold mb-4 text-center">Create Timetable</h2>

        <div className="mb-4">
          <label className="font-medium">Select Class / Group</label>
          <select
            className="w-full mt-2 p-2 rounded-xl border border-gray-300 focus:outline-none"
            value={selectedClass}
            onChange={(e) => setSelectedClass(e.target.value)}
          >
            {classes.length === 0 && <option value="">No classes found</option>}
            {classes.map((c, idx) => {
              const name = getDisplayName(c);
              return (
                <option key={idx} value={name}>
                  {name}
                </option>
              );
            })}
          </select>
        </div>

        <div className="p-4 border rounded-2xl bg-gray-50 mb-4">
          <p className="font-medium mb-2">Subjects</p>
          <ul className="space-y-2">
            {getSubjectsForSelected().length === 0 && (
              <li className="text-sm text-slate-500">No subjects found for selected class</li>
            )}
            {getSubjectsForSelected().map((subj, i) => {
              // 1. Find the specific slot data for THIS subject
              const slot = slots.find((s) => s.subject === subj);
              const teacherId = slot?.teacherId;

              return (
                <li key={i} className="bg-white p-2 shadow rounded-xl flex justify-between items-center">
                  {/* Subject Name */}
                  <span className="font-medium text-slate-700">{subj}</span>

                  {/* Status for this specific subject's teacher */}
                  <div className="min-w-[120px] text-sm flex justify-end">
                    {teacherId ? (
                      (() => {
                        const rec = availabilityMap[String(teacherId)];
                        // Check if record exists and submitted is true
                        if (rec && rec.submitted) {
                          return <span className="text-green-600 font-medium">Responded</span>;
                        }
                        // Otherwise
                        return <span className="text-red-500 font-medium">No response</span>;
                      })()
                    ) : (
                      <span className="text-slate-400 text-xs italic">No teacher selected</span>
                    )}
                  </div>
                </li>
              );
            })}
          </ul>
        </div>

        <div className="space-y-4 mb-4">
          {slots.map((slot, idx) => (
            <div
              key={idx}
              className="flex flex-col gap-2 bg-gray-50 p-3 rounded-xl shadow"
            >
              <div className="flex items-center space-x-2">
                <div className="flex-1">
                  <div className="text-sm font-medium text-slate-700 mb-1">{slot.subject}</div>

                  <div className="flex flex-col gap-2">

                    <input
                      type="number"
                      placeholder="Classes per week (e.g. 3)"
                      className="p-2 rounded-xl border border-gray-300 w-full"
                      value={slot.count}
                      onChange={(e) => {
                        const val = e.target.value;
                        setSlots((prev) =>
                          prev.map((s, i) => (i === idx ? { ...s, count: val } : s))
                        );
                      }}
                    />

                    <div className="flex gap-2">
                      <select
                        className="p-2 rounded-xl border border-gray-300 flex-1"
                        value={slot.teacherId}
                        onChange={(e) => {
                          const value = e.target.value;
                          setSlots((prev) => prev.map((s, i) => (i === idx ? { ...s, teacherId: value } : s)));
                        }}
                      >
                        <option value="">Select teacher</option>
                        {getTeachersForSubject(slot.subject).map((t) => {
                          const id = getTeacherId(t);
                          const label = t.name ?? t.fullname ?? id;
                          return <option key={id} value={id}>{label}</option>;
                        })}
                      </select>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex gap-2 justify-end">
                <button
                  type="button"
                  onClick={async () => {
                    if (!slot.teacherId) return alert('Select a teacher first');
                    try {
                      const teacherIdStr = String(slot.teacherId);
                      const payload = { teacher_id: teacherIdStr };

                      const res = await fetch(`${API_BASE}/api/teachers/generate-link`, {
                        method: 'POST',
                        headers: {
                          'Content-Type': 'application/json',
                        },
                        credentials: 'include',
                        body: JSON.stringify(payload),
                      });

                      if (!res.ok) {
                        const text = await res.text();
                        alert(text || 'Failed to send');
                      } else {
                        alert('Sent successfully');
                      }
                    } catch (err) {
                      console.error(err);
                      alert('Error sending');
                    }
                  }}
                  className="bg-green-600 text-white px-3 py-1 rounded-md"
                >
                  Send
                </button>

                <button
                  type="button"
                  onClick={() => {
                    setSlots((prev) => prev.map((s, i) => (i === idx ? { ...s, teacherId: "" } : s)));
                  }}
                  className="bg-gray-200 text-slate-800 px-3 py-1 rounded-md"
                >
                  Cancel
                </button>
              </div>
            </div>
          ))}
        </div>
        <button
          onClick={() => {
            const payload = generateTimetableJSON();
            if (!payload.studentgroups[0].group) {
              alert("Please select a class.");
              return;
            }
            submitTimetableData(payload);
          }}
          className="w-full bg-blue-600 text-white p-3 rounded-2xl shadow hover:bg-blue-700 transition"
        >
          Submit
        </button>
      </div>
    </div>
  );
}