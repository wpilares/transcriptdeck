import axios from "axios";

/** Shared HTTP client. Every request goes to the API through the "/api" proxy. */
export const axiosInstance = axios.create({
  baseURL: "/api",
  timeout: 10_000,
});
