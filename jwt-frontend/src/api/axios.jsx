import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// 🔹 Attach access token
API.interceptors.request.use((req) => {
  const access = localStorage.getItem("access_token");

  if (access) {
    req.headers.Authorization = `Bearer ${access}`;
  }

  return req;
});

// 🔹 Handle refresh
API.interceptors.response.use(
  (res) => res,
  async (err) => {
    const original = err.config;

    if (!original) return Promise.reject(err);

    if (original.url.includes("/auth/refresh")) {
      return Promise.reject(err);
    }

    if (err.response?.status === 401 && !original._retry) {
      original._retry = true;

      const refresh = localStorage.getItem("refresh_token");

      if (!refresh) {
        localStorage.clear();
        window.location.href = "/";
        return Promise.reject(err);
      }

      try {
        const res = await API.post("/auth/refresh", {
          refresh_token: refresh,
        });

        const newAccess = res.data.access_token;

        localStorage.setItem("access_token", newAccess);

        // Retry original request
        original.headers.Authorization = `Bearer ${newAccess}`;

        return API(original);
      } catch (e) {
        localStorage.clear();
        window.location.href = "/";
      }
    }

    return Promise.reject(err);
  }
);

export default API;