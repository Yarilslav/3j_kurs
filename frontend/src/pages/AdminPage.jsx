import { useEffect, useState } from "react";
import { useOutletContext } from "react-router-dom";

import { fetchOrders, updateOrderStatus } from "../api/orders";
import { createProduct, deleteProduct, fetchProducts, updateProduct } from "../api/products";
import { fetchReservations, updateReservationStatus } from "../api/reservations";
import { deleteUser, fetchUsers, updateUserRole } from "../api/users";
import StatusBox from "../components/StatusBox";

const adminTabs = [
  { id: "products", label: "Товари" },
  { id: "users", label: "Користувачі" },
  { id: "orders", label: "Замовлення" },
  { id: "reservations", label: "Бронювання" },
];

const roleOptions = ["user", "staff", "admin"];
const statusOptions = ["pending", "confirmed", "completed", "cancelled"];

const initialProduct = {
  name: "",
  native_name: "",
  image_filename: "",
  kind: "",
  categories: "",
  description: "",
  price_uah: 0,
  stock_quantity: 0,
};

export default function AdminPage() {
  const { currentUser } = useOutletContext();
  const [activeTab, setActiveTab] = useState("products");
  const [products, setProducts] = useState([]);
  const [users, setUsers] = useState([]);
  const [orders, setOrders] = useState([]);
  const [reservations, setReservations] = useState([]);
  const [form, setForm] = useState(initialProduct);
  const [editingId, setEditingId] = useState(null);
  const [status, setStatus] = useState("");
  const [tone, setTone] = useState("neutral");

  const canOpenAdmin = currentUser && ["admin", "staff"].includes(currentUser.role);

  async function loadProducts() {
    const result = await fetchProducts();
    setProducts(result);
  }

  async function loadUsers() {
    if (currentUser?.role !== "admin") {
      setUsers([]);
      return;
    }
    const result = await fetchUsers();
    setUsers(result);
  }

  async function loadOrders() {
    const result = await fetchOrders();
    setOrders(result);
  }

  async function loadReservations() {
    const result = await fetchReservations();
    setReservations(result);
  }

  async function loadAdminData() {
    try {
      await Promise.all([loadProducts(), loadUsers(), loadOrders(), loadReservations()]);
    } catch (error) {
      setTone("warning");
      setStatus(error.message);
    }
  }

  useEffect(() => {
    if (canOpenAdmin) {
      loadAdminData();
    }
  }, [canOpenAdmin, currentUser?.role]);

  function startEdit(product) {
    setEditingId(product.id);
    setForm({
      name: product.name,
      native_name: product.native_name || "",
      image_filename: product.image_filename || "",
      kind: product.kind,
      categories: product.categories.join(", "),
      description: product.description || "",
      price_uah: product.price_uah,
      stock_quantity: product.stock_quantity,
    });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    const payload = {
      ...form,
      price_uah: Number(form.price_uah),
      stock_quantity: Number(form.stock_quantity),
    };

    try {
      if (editingId) {
        await updateProduct(editingId, payload);
        setStatus(`Product #${editingId} updated.`);
      } else {
        await createProduct(payload);
        setStatus("Product created.");
      }
      setTone("success");
      setEditingId(null);
      setForm(initialProduct);
      await loadProducts();
    } catch (error) {
      setTone("warning");
      setStatus(error.message);
    }
  }

  async function handleDeleteProduct(productId) {
    try {
      await deleteProduct(productId);
      setTone("success");
      setStatus(`Product #${productId} deleted.`);
      await loadProducts();
    } catch (error) {
      setTone("warning");
      setStatus(error.message);
    }
  }

  async function handleRoleChange(login, role) {
    try {
      await updateUserRole(login, role);
      setTone("success");
      setStatus(`Role for ${login} updated.`);
      await loadUsers();
    } catch (error) {
      setTone("warning");
      setStatus(error.message);
    }
  }

  async function handleDeleteUser(userId) {
    try {
      await deleteUser(userId);
      setTone("success");
      setStatus(`User #${userId} deleted.`);
      await loadUsers();
    } catch (error) {
      setTone("warning");
      setStatus(error.message);
    }
  }

  async function handleOrderStatus(orderId, statusValue) {
    try {
      await updateOrderStatus(orderId, statusValue);
      setTone("success");
      setStatus(`Order #${orderId} updated.`);
      await loadOrders();
    } catch (error) {
      setTone("warning");
      setStatus(error.message);
    }
  }

  async function handleReservationStatus(reservationId, statusValue) {
    try {
      await updateReservationStatus(reservationId, statusValue);
      setTone("success");
      setStatus(`Reservation #${reservationId} updated.`);
      await loadReservations();
    } catch (error) {
      setTone("warning");
      setStatus(error.message);
    }
  }

  if (!canOpenAdmin) {
    return (
      <section className="page-stack">
        <div className="section-card">
          <span className="eyebrow">Обмежений доступ</span>
          <h1>Ця сторінка доступна працівникам та адміністраторам</h1>
          <p>Після входу з відповідною роллю тут з'явиться повна панель керування.</p>
        </div>
      </section>
    );
  }

  return (
    <section className="page-stack">
      <div className="section-card__header">
        <span className="eyebrow">Панель керування</span>
        <h1>Користувачі, товари, замовлення і бронювання</h1>
      </div>

      <div className="auth-mode-switch">
        {adminTabs.map((tab) => (
          <button
            key={tab.id}
            type="button"
            className={activeTab === tab.id ? "switch-button switch-button--active" : "switch-button"}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <StatusBox tone={tone} message={status} />

      {activeTab === "products" ? (
        <div className="admin-grid">
          <form className="section-card form-grid" onSubmit={handleSubmit}>
            <h2>{editingId ? `Редагування товару #${editingId}` : "Додавання товару"}</h2>
            <label>
              Назва
              <input value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} required />
            </label>
            <label>
              Назва оригіналом
              <input value={form.native_name} onChange={(event) => setForm({ ...form, native_name: event.target.value })} />
            </label>
            <label>
              Назва файлу картинки
              <input value={form.image_filename} onChange={(event) => setForm({ ...form, image_filename: event.target.value })} />
            </label>
            <label>
              Тип
              <input value={form.kind} onChange={(event) => setForm({ ...form, kind: event.target.value })} required />
            </label>
            <label>
              Категорії
              <input value={form.categories} onChange={(event) => setForm({ ...form, categories: event.target.value })} required />
            </label>
            <label>
              Опис
              <textarea value={form.description} onChange={(event) => setForm({ ...form, description: event.target.value })} rows="4" />
            </label>
            <label>
              Ціна
              <input type="number" min="0" value={form.price_uah} onChange={(event) => setForm({ ...form, price_uah: event.target.value })} required />
            </label>
            <label>
              Кількість
              <input type="number" min="0" value={form.stock_quantity} onChange={(event) => setForm({ ...form, stock_quantity: event.target.value })} required />
            </label>
            <div className="button-row">
              <button className="button button--primary" type="submit">
                {editingId ? "Зберегти зміни" : "Створити товар"}
              </button>
              <button
                className="button"
                type="button"
                onClick={() => {
                  setEditingId(null);
                  setForm(initialProduct);
                }}
              >
                Очистити
              </button>
            </div>
          </form>

          <div className="section-card stack-medium">
            <h2>Поточні товари</h2>
            {products.map((product) => (
              <article key={product.id} className="admin-row-card">
                <div>
                  <strong>{product.name}</strong>
                  <p>{product.kind} · {product.price_uah} грн · {product.stock_quantity} шт.</p>
                </div>
                <div className="button-row">
                  <button className="button" type="button" onClick={() => startEdit(product)}>
                    Редагувати
                  </button>
                  <button className="button button--danger" type="button" onClick={() => handleDeleteProduct(product.id)}>
                    Видалити
                  </button>
                </div>
              </article>
            ))}
          </div>
        </div>
      ) : null}

      {activeTab === "users" ? (
        <div className="section-card stack-medium">
          <h2>Зареєстровані користувачі</h2>
          {currentUser.role !== "admin" ? <p>Редагування користувачів доступне тільки адміну.</p> : null}
          {users.map((user) => (
            <article key={user.id} className="admin-row-card">
              <div>
                <strong>{user.name}</strong>
                <p>{user.login} · {user.email}</p>
              </div>
              <div className="inline-controls">
                <select
                  value={user.role}
                  onChange={(event) => handleRoleChange(user.login, event.target.value)}
                  disabled={currentUser.role !== "admin"}
                >
                  {roleOptions.map((role) => (
                    <option key={role} value={role}>
                      {role}
                    </option>
                  ))}
                </select>
                <button
                  className="button button--danger"
                  type="button"
                  onClick={() => handleDeleteUser(user.id)}
                  disabled={currentUser.role !== "admin"}
                >
                  Видалити
                </button>
              </div>
            </article>
          ))}
        </div>
      ) : null}

      {activeTab === "orders" ? (
        <div className="section-card stack-medium">
          <h2>Замовлення</h2>
          {orders.map((order) => (
            <article key={order.id} className="admin-row-card admin-row-card--stacked">
              <div>
                <strong>Замовлення #{order.id}</strong>
                <p>{order.what_ordered}</p>
                <p>{order.address || "Без адреси"} · {order.total_price} грн</p>
              </div>
              <div className="inline-controls">
                <select value={order.status} onChange={(event) => handleOrderStatus(order.id, event.target.value)}>
                  {statusOptions.map((statusOption) => (
                    <option key={statusOption} value={statusOption}>
                      {statusOption}
                    </option>
                  ))}
                </select>
              </div>
            </article>
          ))}
        </div>
      ) : null}

      {activeTab === "reservations" ? (
        <div className="section-card stack-medium">
          <h2>Бронювання</h2>
          {reservations.map((reservation) => (
            <article key={reservation.id} className="admin-row-card admin-row-card--stacked">
              <div>
                <strong>Бронювання #{reservation.id}</strong>
                <p>{reservation.reservation_at}</p>
                <p>Місця: {reservation.places.join(", ")}</p>
              </div>
              <div className="inline-controls">
                <select
                  value={reservation.status}
                  onChange={(event) => handleReservationStatus(reservation.id, event.target.value)}
                >
                  {statusOptions.map((statusOption) => (
                    <option key={statusOption} value={statusOption}>
                      {statusOption}
                    </option>
                  ))}
                </select>
              </div>
            </article>
          ))}
        </div>
      ) : null}
    </section>
  );
}
