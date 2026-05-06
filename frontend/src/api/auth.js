import { apiRequest } from "./client";

export function registerUser(payload) {
  return apiRequest("/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function loginUser(payload) {
  return apiRequest("/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function fetchMe() {
  return apiRequest("/me");
}
