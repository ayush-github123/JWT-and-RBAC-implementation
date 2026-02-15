import React, { useState } from "react";
import { createTask } from "../api/tasks.jsx";
import TaskList from "../components/TaskList.jsx";

export default function Dashboard() {
  const [task, setTask] = useState({
    title: "",
    description: "",
  });

  const handleCreate = async () => {
    await createTask(task);
    alert("Task created");
    window.location.reload();
  };

  return (
    <div>
      <h2>Dashboard</h2>

      <input
        placeholder="Title"
        onChange={(e) => setTask({ ...task, title: e.target.value })}
      />

      <input
        placeholder="Description"
        onChange={(e) => setTask({ ...task, description: e.target.value })}
      />

      <button onClick={handleCreate}>Create Task</button>

      <TaskList />
    </div>
  );
}