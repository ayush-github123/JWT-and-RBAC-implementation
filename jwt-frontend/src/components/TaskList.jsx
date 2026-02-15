import { useEffect, useState } from "react";
import { getMyTasks, deleteTask } from "../api/tasks.jsx";

export default function TaskList({ refresh }) {
  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [deletingId, setDeletingId] = useState(null);

  const load = async () => {
    setIsLoading(true);
    try {
      const res = await getMyTasks();
      setTasks(res.data);
    } catch (err) {
      console.error("Failed to load tasks:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [refresh]);

  const handleDelete = async (id) => {
    if (!confirm("Are you sure you want to delete this task?")) return;
    
    setDeletingId(id);
    try {
      await deleteTask(id);
      await load();
    } catch (err) {
      alert("Failed to delete task");
    } finally {
      setDeletingId(null);
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <svg
          className="mx-auto h-16 w-16 text-gray-400 mb-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          />
        </svg>
        <h3 className="text-lg font-medium text-gray-900 mb-1">No tasks yet</h3>
        <p className="text-gray-600">Create your first task to get started!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {tasks.map((t) => (
        <div
          key={t.id}
          className="border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow bg-white"
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h4 className="text-lg font-semibold text-gray-900 mb-2">{t.title}</h4>
              {t.description && (
                <p className="text-gray-600 mb-3">{t.description}</p>
              )}
              <div className="flex items-center gap-2 text-sm text-gray-500">
                <svg
                  className="h-4 w-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <span>Created {new Date(t.createdAt || Date.now()).toLocaleDateString()}</span>
              </div>
            </div>
            
            <button
              onClick={() => handleDelete(t.id)}
              disabled={deletingId === t.id}
              className="ml-4 px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg font-medium transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {deletingId === t.id ? "Deleting..." : "Delete"}
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}