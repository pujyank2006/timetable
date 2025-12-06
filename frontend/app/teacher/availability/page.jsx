"use client";

import React, { useState, useEffect } from 'react';
const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
const hours = ["9-10", "10-11", "11-12", "12-1", "2-3", "3-4", "4-5"];

const getTokenFromUrl = () => {
    const params = new URLSearchParams(window.location.search);
    return params.get('token'); 
};

const styles = {
    body: {
        fontFamily: 'Arial',
        margin: '20px',
    },
    day: {
        margin: '20px 0',
    },
    slot: {
        display: 'inline-block',
        padding: '10px',
        margin: '5px',
        border: '1px solid #ccc',
        borderRadius: '6px',
        cursor: 'pointer',
    },
    selected: {
        background: '#ff7675',
        color: 'white',
    },
    button: {
        marginTop: '20px',
        padding: '10px 20px',
        fontSize: '16px',
    }
};


const TeacherAvailability = () => {
    const [unavailability, setUnavailability] = useState(() => {
        const initial = {};
        days.forEach(day => {
            initial[day] = new Array(hours.length).fill(0);
        });
        return initial;
    });
    
    const [token, setToken] = useState(null);
    useEffect(() => {
        setToken(getTokenFromUrl());
    }, []);


    const handleSlotClick = (dayName, index) => {
        setUnavailability(prevUnavailability => {
            const newDaySlots = [...prevUnavailability[dayName]];
            newDaySlots[index] = newDaySlots[index] === 0 ? 1 : 0;
            
            return {
                ...prevUnavailability,
                [dayName]: newDaySlots,
            };
        });
    };

    const submitData = () => {
        if (!token) {
            alert("Error: Missing token. Cannot submit availability.");
            return;
        }

        const payload = {
            token: token,
            availability: unavailability,
            submitted: true
        };

        fetch("/availability/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        })
        .then(res => {
            if (!res.ok) {
                return res.json().then(err => Promise.reject(err));
            }
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
            {token ? (
                <p>Token: {token}</p>
            ) : (
                <p style={{color: 'red'}}>Loading token...</p>
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
                disabled={!token}
            >
                Submit
            </button>
        </div>
    );
};

export default TeacherAvailability;