import { createContext, useContext, useEffect, useState } from "react";

const AuthContext = createContext();

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const response = await fetch(`${API_BASE}/users/me`, {
                    method: "GET",
                    credentials: "include", // Include cookies
                    headers: {
                        "Content-Type": "application/json",
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    setUser(data.user);
                } else {
                    setUser(null);
                }
            } catch (error) {
                console.error("Auth check failed:", error);
                setUser(null);
            } finally {
                setLoading(false);
            }
        };

        checkAuth();
    }, []);
    const login = (userData) => {
        setUser(userData); // Set user immediately for a smooth transition
    };

    const logout = () => {
        setUser(null);
        // Add logic to clear cookies via backend call if needed
    };
    return (
        <AuthContext.Provider value={{ user, loading, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
