"use client";

import React, { useState, useEffect } from 'react';

const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
const hours = ["9-10", "10-11", "11-12", "12-1", "2-3", "3-4", "4-5"];

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;

// UPDATED FUNCTION: Handles standard '&' and non-standard '?' separators
const getTeacherIdFromUrl = () => {
    if (typeof window !== "undefined") {
        const search = window.location.search;
        
        // 1. Try standard parsing first
        const params = new URLSearchParams(search);
        let id = params.get('teacher_id');

        // 2. Fallback: Manually parse if URL is malformed like "?token=...?teacher_id=..."
        if (!id && search.includes('teacher_id=')) {
            // Split by 'teacher_id=' and take the part after it
            const parts = search.split('teacher_id=');
            if (parts.length > 1) {
                // If there are more params after (separated by &), remove them
                id = parts[1].split('&')[0];
            }
        }
        
        return id;
    }
    return null;
};

const styles = {
    body: { fontFamily: 'Arial', margin: '20px' },
    day: { margin: '20px 0' },
    slot: {
        display: 'inline-block',
        padding: '10px',
        margin: '5px',
        border: '1px solid #ccc',
        borderRadius: '6px',
        cursor: 'pointer',
    },
    selected: { background: '#ff7675', color: 'white' },
    button: { marginTop: '20px', padding: '10px 20px', fontSize: '16px', background: '#75afffff', borderRadius: '20px'}
};

const TeacherAvailability = () => {
    const [unavailability, setUnavailability] = useState(() => {
        const initial = {};
        days.forEach(day => {
            initial[day] = new Array(hours.length).fill(0);
        });
        return initial;
    });

    const [teacherId, setTeacherId] = useState(null);

    useEffect(() => {
        const id = getTeacherIdFromUrl();
        console.log("Extracted Teacher ID:", id); // Debug log to verify extraction
        setTeacherId(id);
    }, []);

    const handleSlotClick = (dayName, index) => {
        setUnavailability(prev => {
            const newDaySlots = [...prev[dayName]];
            newDaySlots[index] = newDaySlots[index] === 0 ? 1 : 0;
            return { ...prev, [dayName]: newDaySlots };
        });
    };

    const submitData = () => {
        if (!teacherId) {
            alert("Error: Missing teacher_id in URL. Cannot submit.");
            return;
        }

        const selectedSlots = [];
        days.forEach((day, dayIndex) => {
            const daySlots = unavailability[day];
            daySlots.forEach((isSelected, hourIndex) => {
                if (isSelected === 1) {
                    const flatIndex = (dayIndex * hours.length) + hourIndex;
                    selectedSlots.push(flatIndex);
                }
            });
        });

        const payload = {
            teacher_id: teacherId, 
            slots: selectedSlots, 
            submitted: true 
        };

        console.log("Submitting payload:", payload);

        fetch(`${API_BASE}/availability/submit`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: 'include',
            body: JSON.stringify(payload)
        })
        .then(res => {
            if (!res.ok) return res.json().then(err => Promise.reject(err));
            return res.json();
        })
        .then(data => {
            alert("Submitted Successfully!");
            console.log("Response:", data);
        })
        .catch(error => {
            console.error("Submission failed:", error);
            alert(`Submission Failed: ${error.message || JSON.stringify(error)}`);
        });
    };

    return (
        <div style={styles.body}>
            <h2>Mark Your NOT-AVAILABLE Hours</h2>
            <h3>Consider the recently released timetable</h3>
            {teacherId ? (
                <p>Teacher ID: <strong>{teacherId}</strong></p>
            ) : (
                <p style={{ color: 'red' }}>Loading ID from URL...</p>
            )}

            <div id="container">
                {days.map((dayName, dayIndex) => (
                    <div key={dayIndex} style={styles.day}>
                        <h3>{dayName}</h3>
                        {hours.map((hr, hourIndex) => {
                            const isSelected = unavailability[dayName][hourIndex] === 1;
                            const slotStyle = {
                                ...styles.slot,
                                ...(isSelected ? styles.selected : {})
                            };

                            return (
                                <div
                                    key={hourIndex}
                                    style={slotStyle}
                                    onClick={() => handleSlotClick(dayName, hourIndex)}
                                >
                                    {hr}
                                </div>
                            );
                        })}
                    </div>
                ))}
            </div>

            <button
                style={styles.button}
                onClick={submitData}
                disabled={!teacherId}
            >
                Submit Availability
            </button>
        </div>
    );
};

export default TeacherAvailability;