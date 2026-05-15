import { useEffect, useMemo, useState } from "react";
import { Link, useOutletContext } from "react-router-dom";

import { fetchOrders, createOrder } from "../api/orders";
import { fetchProducts } from "../api/products";
import StatusBox from "../components/StatusBox";
import {
  clearOrderDraft,
  loadOrderDraft,
  saveOrderDraft,
} from "../utils/orderDraft";
import { getProductImage } from "../utils/productAssets";

function getAccountDraftKey(currentUser) {
  return currentUser?.login || "guest";
}

export default function OrderPage() {
  const { currentUser } = useOutletContext();
  const accountDraftKey = getAccountDraftKey(currentUser);
  const [draft, setDraft] = useState(() => loadOrderDraft(accountDraftKey));
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [status, setStatus] = useState("");
  const [tone, setTone] = useState("neutral");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setDraft(loadOrderDraft(accountDraftKey));
  }, [accountDraftKey]);

  useEffect(() => {
    if (!currentUser) {
      return;
    }

    setDraft((currentDraft) => ({
      ...currentDraft,
      guestName: currentDraft.guestName || currentUser.name || "",
      guestContact: currentDraft.guestContact || currentUser.phone_number || "",
      address: currentDraft.address || currentUser.address || "",
    }));
  }, [currentUser]);

  useEffect(() => {
    saveOrderDraft(accountDraftKey, draft);
  }, [accountDraftKey, draft]);

  useEffect(() => {
    async function loadProducts() {
      try {
        const result = await fetchProducts();
        setProducts(result);
      } catch (error) {
        setTone("warning");
        setStatus(error.message);
      }
    }

    loadProducts();
  }, []);

  useEffect(() => {
    async function loadOrdersForUser() {
      if (!currentUser) {
        setOrders([]);
        return;
      }

      try {
        const result = await fetchOrders();
        setOrders(result);
      } catch {
        setOrders([]);
      }
    }

    loadOrdersForUser();
  }, [currentUser]);

  const detailedItems = useMemo(
    () =>
      draft.items
        .map((item) => {
          const product = products.find((entry) => entry.id === item.productId);
          if (!product) {
            return null;
          }

          return {
            ...item,
            product,
            lineTotal: item.quantity * product.price_uah,
          };
        })
        .filter(Boolean),
    [draft.items, products],
  );

  const totalPrice = detailedItems.reduce((sum, item) => sum + item.lineTotal, 0);

  function updateItemQuantity(productId, quantity) {
    if (quantity <= 0) {
      setDraft((currentDraft) => ({
        ...currentDraft,
        items: currentDraft.items.filter((item) => item.productId !== productId),
      }));
      return;
    }

    setDraft((currentDraft) => ({
      ...currentDraft,
      items: currentDraft.items.map((item) =>
        item.productId === productId ? { ...item, quantity } : item,
      ),
    }));
  }

  function handleRemoveItem(productId) {
    setDraft((currentDraft) => ({
      ...currentDraft,
      items: currentDraft.items.filter((item) => item.productId !== productId),
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setStatus("");

    try {
      const payload = {
        items: draft.items.map((item) => ({
          product_id: item.productId,
          quantity: item.quantity,
        })),
        address: draft.fulfillmentType === "delivery" ? draft.address : undefined,
        guest_name: currentUser ? undefined : draft.guestName,
        guest_contact: currentUser ? undefined : draft.guestContact,
      };

      const result = await createOrder(payload);
      setTone("success");
      setStatus(`Замовлення #${result.id} створено. Загальна сума: ${result.total_price} грн.`);
      const emptyDraft = {
        ...draft,
        items: [],
        address: "",
      };
      setDraft(emptyDraft);
      clearOrderDraft(accountDraftKey);

      if (currentUser) {
        const latestOrders = await fetchOrders();
        setOrders(latestOrders);
      }
    } catch (error) {
      setTone("warning");
      setStatus(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="page-stack">
      <div className="section-card__header">
        <h1>Формування замовлення</h1>
      </div>

      <div className="order-page-layout">
        <form className="order-builder" onSubmit={handleSubmit}>
          <div className="order-builder__header">
            <h2>Формування замовлення</h2>
          </div>

          <div className="order-builder__body">
            <div className="order-lines">
              {detailedItems.length ? (
                detailedItems.map((item, index) => {
                  const productImage = getProductImage(item.product);

                  return (
                    <article key={item.productId} className="order-line">
                      <span className="order-line__index">{index + 1})</span>
                      <div className="order-line__visual">
                        {productImage ? (
                          <img src={productImage} alt={item.product.name} />
                        ) : (
                          <span>Іконка товару</span>
                        )}
                      </div>
                      <div className="order-line__details">
                        <strong>{item.product.name}</strong>
                        <span>Кількість</span>
                        <input
                          type="number"
                          min="1"
                          value={item.quantity}
                          onChange={(event) =>
                            updateItemQuantity(item.productId, Number(event.target.value))
                          }
                        />
                        <span>{item.lineTotal} грн</span>
                      </div>
                      <button
                        type="button"
                        className="pill-button pill-button--danger"
                        onClick={() => handleRemoveItem(item.productId)}
                      >
                        Вилучити
                      </button>
                    </article>
                  );
                })
              ) : (
                <div className="order-builder__empty">
                  <p>Список поки порожній. Додайте товари з каталогу.</p>
                </div>
              )}

              <Link className="pill-button order-builder__add" to="/catalog">
                Додати товар
              </Link>
            </div>

            <div className="order-sidebar-controls">
              <div className="order-type-card">
                <h3>Тип замовлення</h3>
                <div className="auth-mode-switch">
                  <button
                    type="button"
                    className={
                      draft.fulfillmentType === "pickup"
                        ? "switch-button switch-button--active"
                        : "switch-button"
                    }
                    onClick={() =>
                      setDraft((currentDraft) => ({
                        ...currentDraft,
                        fulfillmentType: "pickup",
                        address: "",
                      }))
                    }
                  >
                    В закладі
                  </button>
                  <button
                    type="button"
                    className={
                      draft.fulfillmentType === "delivery"
                        ? "switch-button switch-button--active"
                        : "switch-button"
                    }
                    onClick={() =>
                      setDraft((currentDraft) => ({
                        ...currentDraft,
                        fulfillmentType: "delivery",
                        address: currentUser?.address || currentDraft.address,
                      }))
                    }
                  >
                    Доставка
                  </button>
                </div>
              </div>

              <div className="order-contact-card">
                <label>
                  Контактні дані
                  <input
                    value={draft.guestContact}
                    onChange={(event) =>
                      setDraft((currentDraft) => ({
                        ...currentDraft,
                        guestContact: event.target.value,
                      }))
                    }
                    placeholder="+380..."
                  />
                </label>

                {!currentUser ? (
                  <label>
                    Ім'я
                    <input
                      value={draft.guestName}
                      onChange={(event) =>
                        setDraft((currentDraft) => ({
                          ...currentDraft,
                          guestName: event.target.value,
                        }))
                      }
                      placeholder="Ваше ім'я"
                    />
                  </label>
                ) : null}

                {draft.fulfillmentType === "delivery" ? (
                  <label>
                    Введіть адресу
                    <input
                      value={draft.address}
                      onChange={(event) =>
                        setDraft((currentDraft) => ({
                          ...currentDraft,
                          address: event.target.value,
                        }))
                      }
                      placeholder="Адреса доставки"
                    />
                  </label>
                ) : null}
              </div>

              <div className="order-total-card">
                <div className="order-total-card__value">Загальна ціна: {totalPrice} грн</div>
                <button
                  className="pill-button pill-button--primary order-total-card__submit"
                  type="submit"
                  disabled={loading || !detailedItems.length}
                >
                  {loading ? "Зберігаємо..." : "Затвердити"}
                </button>
              </div>
            </div>
          </div>

          <StatusBox tone={tone} message={status} />
        </form>

        <aside className="section-card stack-medium">
          <div className="section-pill">Ваші замовлення</div>
          {currentUser ? (
            orders.length ? (
              orders.map((order) => (
                <article key={order.id} className="admin-row-card admin-row-card--stacked">
                  <strong>Замовлення #{order.id}</strong>
                  <p>{order.what_ordered}</p>
                  <p>Статус: {order.status}</p>
                </article>
              ))
            ) : (
              <p>Поки що замовлень немає.</p>
            )
          ) : (
            <p>Після входу тут з'явиться історія ваших замовлень.</p>
          )}
        </aside>
      </div>
    </section>
  );
}
