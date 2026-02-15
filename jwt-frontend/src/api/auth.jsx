import API from "./axios";

export const registerUser = (data) =>
  API.post("/auth/register", data);

export const loginUser = async (data) => {
  const res = await API.post("/auth/login", data);

  localStorage.setItem("access_token", res.data.access_token);
  localStorage.setItem("refresh_token", res.data.refresh_token);

  return res;
};

export const logoutUser = async () => {
  const refresh = localStorage.getItem("refresh_token");

  if (refresh) {
    await API.post("/auth/logout", { refresh_token: refresh });
  }

  localStorage.clear();
};