import { useState } from "react";
import { createTask } from "../api/tasks.jsx";
import TaskList from "../components/TaskList.jsx";

export default function Dashboard() {
  const [task, setTask] = useState({
    title: "",
    description: "",
  });
  const [refresh, setRefresh] = useState(false);
  const [isCreating, setIsCreating] = useState(false);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!task.title.trim()) {
      alert("Please enter a task title");
      return;
    }
    
    setIsCreating(true);
    try {
      await createTask(task);
      setTask({ title: "", description: "" });
      setRefresh(!refresh);
    } catch (err) {
      alert("Failed to create task");
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">Manage your tasks efficiently</p>
        </div>

        {/* Create Task Card */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">Create New Task</h2>
          
          <form onSubmit={handleCreate} className="space-y-4">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                Task Title
              </label>
              <input
                id="title"
                type="text"
                placeholder="Enter task title..."
                value={task.title}
                onChange={(e) => setTask({ ...task, title: e.target.value })}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
              />
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                id="description"
                placeholder="Enter task description..."
                value={task.description}
                onChange={(e) => setTask({ ...task, description: e.target.value })}
                rows={4}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition resize-none"
              />
            </div>

            <button
              type="submit"
              disabled={isCreating}
              className="w-full sm:w-auto px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isCreating ? "Creating..." : "Create Task"}
            </button>
          </form>
        </div>

        {/* Task List */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">Your Tasks</h2>
          <TaskList refresh={refresh} />
        </div>
      </div>
    </div>
  );
}