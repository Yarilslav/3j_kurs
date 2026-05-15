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

export function updateOrderStatus(orderId, status) {
  return apiRequest(`/orders/${orderId}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status }),
  });
}
