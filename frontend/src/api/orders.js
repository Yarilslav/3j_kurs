import { apiRequest } from "./client";

export function createOrder(payload) {
  return apiRequest("/orders/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function fetchOrders() {
  return apiRequest("/orders/");
}
