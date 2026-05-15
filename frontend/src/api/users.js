import { apiRequest } from "./client";

export function fetchUsers() {
  return apiRequest("/users/");
}

export function deleteUser(userId) {
  return apiRequest(`/users/${userId}`, {
    method: "DELETE",
  });
}

export function updateUserRole(login, role) {
  return apiRequest(`/users/by-login/${login}/role`, {
    method: "PATCH",
    body: JSON.stringify({ role }),
  });
}
