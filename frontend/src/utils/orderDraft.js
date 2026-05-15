const DEFAULT_DRAFT = {
  items: [],
  fulfillmentType: "pickup",
  guestName: "",
  guestContact: "",
  address: "",
};

function normalizeDraft(draft) {
  if (!draft || typeof draft !== "object") {
    return { ...DEFAULT_DRAFT };
  }

  return {
    items: Array.isArray(draft.items) ? draft.items : [],
    fulfillmentType: draft.fulfillmentType === "delivery" ? "delivery" : "pickup",
    guestName: draft.guestName || "",
    guestContact: draft.guestContact || "",
    address: draft.address || "",
  };
}

export function getDraftStorageKey(accountKey) {
  return `asahi-order-draft:${accountKey || "guest"}`;
}

export function loadOrderDraft(accountKey) {
  if (typeof window === "undefined") {
    return { ...DEFAULT_DRAFT };
  }

  try {
    const raw = window.localStorage.getItem(getDraftStorageKey(accountKey));
    return normalizeDraft(raw ? JSON.parse(raw) : null);
  } catch {
    return { ...DEFAULT_DRAFT };
  }
}

export function saveOrderDraft(accountKey, draft) {
  if (typeof window === "undefined") {
    return;
  }

  window.localStorage.setItem(
    getDraftStorageKey(accountKey),
    JSON.stringify(normalizeDraft(draft)),
  );
}

export function clearOrderDraft(accountKey) {
  if (typeof window === "undefined") {
    return;
  }

  window.localStorage.removeItem(getDraftStorageKey(accountKey));
}

export function addItemToDraft(draft, productId) {
  const normalized = normalizeDraft(draft);
  const existingItem = normalized.items.find((item) => item.productId === productId);

  if (existingItem) {
    return {
      ...normalized,
      items: normalized.items.map((item) =>
        item.productId === productId
          ? { ...item, quantity: item.quantity + 1 }
          : item,
      ),
    };
  }

  return {
    ...normalized,
    items: [...normalized.items, { productId, quantity: 1 }],
  };
}
