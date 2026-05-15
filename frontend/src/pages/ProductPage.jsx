import { useEffect, useState } from "react";
import { Link, useOutletContext, useParams } from "react-router-dom";

import { createOrder } from "../api/orders";
import { fetchProduct } from "../api/products";
import StatusBox from "../components/StatusBox";
import { addItemToDraft, loadOrderDraft, saveOrderDraft } from "../utils/orderDraft";
import { getProductImage } from "../utils/productAssets";

const initialOrder = {
  quantity: 1,
  address: "",
  guest_name: "",
  guest_contact: "",
};

export default function ProductPage() {
  const { currentUser } = useOutletContext();
  const { productId } = useParams();
  const [product, setProduct] = useState(null);
  const [orderForm, setOrderForm] = useState(initialOrder);
  const [status, setStatus] = useState("");
  const [tone, setTone] = useState("neutral");

  useEffect(() => {
    async function loadProduct() {
      try {
        const result = await fetchProduct(productId);
        setProduct(result);
      } catch (error) {
        setTone("warning");
        setStatus(error.message);
      }
    }

    loadProduct();
  }, [productId]);

  async function handleSubmit(event) {
    event.preventDefault();
    setStatus("");
    try {
      const result = await createOrder({
        items: [{ product_id: Number(productId), quantity: Number(orderForm.quantity) }],
        address: orderForm.address,
        guest_name: orderForm.guest_name || undefined,
        guest_contact: orderForm.guest_contact || undefined,
      });
      setTone("success");
      setStatus(`Order #${result.id} created. Total: ${result.total_price} UAH.`);
      setOrderForm(initialOrder);
    } catch (error) {
      setTone("warning");
      setStatus(error.message);
    }
  }

  function handleAddToDraft() {
    const accountKey = currentUser?.login || "guest";
    const nextDraft = addItemToDraft(loadOrderDraft(accountKey), Number(productId));
    saveOrderDraft(accountKey, nextDraft);
    setTone("success");
    setStatus("Товар додано до списку формування замовлення.");
  }

  return (
    <section className="page-stack">
      <div className="section-card__header">
        <span className="eyebrow">Сторінка продукту</span>
        <h1>Окрема позиція і швидке створення замовлення</h1>
      </div>

      {!product ? (
        <div className="section-card">
          <p>Завантаження продукту...</p>
        </div>
      ) : (
        <div className="product-layout">
          <article className="section-card stack-medium">
            <div className="product-hero">
              <div className="product-hero__media">
                {getProductImage(product) ? (
                  <img src={getProductImage(product)} alt={product.name} />
                ) : (
                  <span>Картинка</span>
                )}
              </div>
              <div>
                <h2>{product.name}</h2>
                <p>{product.native_name || "No native title"}</p>
                <div className="button-row">
                  <button className="button button--soft-accent" type="button" onClick={handleAddToDraft}>
                    Додати в замовлення
                  </button>
                  <Link className="button button--ghost" to="/order">
                    Перейти до замовлення
                  </Link>
                </div>
              </div>
            </div>
            <div>
              <p>{product.description || "No description yet."}</p>
            </div>
            <dl className="data-list">
              <div>
                <dt>Тип</dt>
                <dd>{product.kind}</dd>
              </div>
              <div>
                <dt>Категорії</dt>
                <dd>{product.categories.join(", ")}</dd>
              </div>
              <div>
                <dt>Ціна</dt>
                <dd>{product.price_uah} грн</dd>
              </div>
              <div>
                <dt>Залишок</dt>
                <dd>{product.stock_quantity}</dd>
              </div>
              <div>
                <dt>Файл зображення</dt>
                <dd>{product.image_filename || "Не вказано"}</dd>
              </div>
            </dl>
          </article>

          <form className="section-card form-grid" onSubmit={handleSubmit}>
            <h2>Оформлення замовлення</h2>
            <label>
              Кількість
              <input
                type="number"
                min="1"
                value={orderForm.quantity}
                onChange={(event) => setOrderForm({ ...orderForm, quantity: event.target.value })}
                required
              />
            </label>
            <label>
              Адреса доставки
              <input
                value={orderForm.address}
                onChange={(event) => setOrderForm({ ...orderForm, address: event.target.value })}
                required
              />
            </label>
            <label>
              Ім'я гостя
              <input
                value={orderForm.guest_name}
                onChange={(event) => setOrderForm({ ...orderForm, guest_name: event.target.value })}
              />
            </label>
            <label>
              Контакт
              <input
                value={orderForm.guest_contact}
                onChange={(event) => setOrderForm({ ...orderForm, guest_contact: event.target.value })}
              />
            </label>
            <button className="button button--primary" type="submit">
              Створити замовлення
            </button>
            <StatusBox tone={tone} message={status} />
          </form>
        </div>
      )}
    </section>
  );
}
