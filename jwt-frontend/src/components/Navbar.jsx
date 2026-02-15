import { Link, useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

export default function Navbar() {
  const { user, logout, isAuthenticated, loading } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/");
  };


  if (loading) return null;

  if (!isAuthenticated) return null;

  return (
    <nav className="w-full bg-white shadow-md px-6 py-4 flex justify-between items-center">
      {/* Left */}
      <div className="flex items-center gap-6">
        <h1 className="text-xl font-bold text-blue-600">TaskApp</h1>

        <Link
          to="/dashboard"
          className="text-gray-700 hover:text-blue-600 font-medium"
        >
          Dashboard
        </Link>

        {/* 🔹 ADMIN ONLY */}
        {user?.role === "ADMIN" && (
          <Link
            to="/admin"
            className="text-gray-700 hover:text-blue-600 font-medium"
          >
            Admin Panel
          </Link>
        )}
      </div>

      {/* Right */}
      <div className="flex items-center gap-4">
        <span className="text-gray-600 text-sm">
          {user?.email || "User"}
        </span>

        <button
          onClick={handleLogout}
          className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition"
        >
          Logout
        </button>
      </div>
    </nav>
  );
}