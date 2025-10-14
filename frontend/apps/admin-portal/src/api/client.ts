import axios from "axios";
import { useAuthStore } from "../store/auth-store";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  const tenantId = useAuthStore.getState().user?.tenantId;
  if (tenantId) {
    config.headers = config.headers ?? {};
    config.headers["X-Tenant-ID"] = tenantId;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().clearSession();
    }
    return Promise.reject(error);
  }
);

export { api };
