import API from "./axios";

export const createTask = (data) =>
  API.post("/tasks/", data);

export const getMyTasks = () =>
  API.get("/tasks/?skip=0&limit=10");

export const getAllTasks = () =>
  API.get("/tasks/all");

export const updateTask = (id, data) =>
  API.put(`/tasks/${id}`, data);

export const deleteTask = (id) =>
  API.delete(`/tasks/${id}`);