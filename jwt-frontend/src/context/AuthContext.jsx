import { createContext, useState, useEffect } from "react";
import API from "../api/axios.jsx";

export const AuthContext = createContext();

export default function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const isAuthenticated = !!localStorage.getItem("access_token");

  // 🔹 Fetch user on app load
  useEffect(() => {
    const fetchUser = async () => {
      try {
        if (isAuthenticated) {
          const res = await API.get("/auth/me");
          setUser(res.data);
          console.log(res.data)
        }
      } catch (err) {
        console.log("Failed to fetch user", err);
        localStorage.clear();
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  // 🔹 Login
  const login = async (data) => {
    const res = await API.post("/auth/login", data);

    localStorage.setItem("access_token", res.data.access_token);
    localStorage.setItem("refresh_token", res.data.refresh_token);

    // fetch user after login
    const userRes = await API.get("/auth/me");
    setUser(userRes.data);
  };

  // 🔹 Logout
  const logout = async () => {
    try {
      const refresh = localStorage.getItem("refresh_token");

      if (refresh) {
        await API.post("/auth/logout", { refresh_token: refresh });
      }
    } catch {}

    localStorage.clear();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated, loading }}>
      {children}
    </AuthContext.Provider>
  );
}