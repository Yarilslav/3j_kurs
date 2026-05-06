import { apiRequest } from "./client";

export function fetchProducts() {
  return apiRequest("/products/");
}

export function fetchProduct(productId) {
  return apiRequest(`/products/${productId}`);
}

export function createProduct(payload) {
  return apiRequest("/products/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateProduct(productId, payload) {
  return apiRequest(`/products/${productId}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

export function deleteProduct(productId) {
  return apiRequest(`/products/${productId}`, {
    method: "DELETE",
  });
}
