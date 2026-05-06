import { apiRequest } from "./client";

export function createReservation(payload) {
  return apiRequest("/reservations/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function fetchReservations() {
  return apiRequest("/reservations/");
}
