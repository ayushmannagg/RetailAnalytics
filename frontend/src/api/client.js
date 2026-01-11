import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.PROD ? "" : "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export default apiClient;
