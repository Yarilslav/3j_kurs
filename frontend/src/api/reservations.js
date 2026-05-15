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

export function updateReservationStatus(reservationId, status) {
  return apiRequest(`/reservations/${reservationId}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status }),
  });
}
