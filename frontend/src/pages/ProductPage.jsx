import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { createOrder } from "../api/orders";
import { fetchProduct } from "../api/products";
import StatusBox from "../components/StatusBox";

const initialOrder = {
  quantity: 1,
  address: "",
  guest_name: "",
  guest_contact: "",
};

export default function ProductPage() {
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

  return (
    <section className="stack-large">
      <div className="page-header">
        <span className="eyebrow">Route /catalog/:id</span>
        <h1>Product details + order flow</h1>
      </div>

      {!product ? (
        <div className="panel">
          <p>Loading product...</p>
        </div>
      ) : (
        <div className="two-column two-column--wide">
          <article className="panel stack-medium">
            <div>
              <span className="eyebrow">Tea #{product.id}</span>
              <h2>{product.name}</h2>
              <p>{product.native_name || "No native title"}</p>
            </div>
            <p>{product.description || "No description yet."}</p>
            <dl className="data-list">
              <div>
                <dt>Kind</dt>
                <dd>{product.kind}</dd>
              </div>
              <div>
                <dt>Categories</dt>
                <dd>{product.categories.join(", ")}</dd>
              </div>
              <div>
                <dt>Price</dt>
                <dd>{product.price_uah} UAH</dd>
              </div>
              <div>
                <dt>Stock</dt>
                <dd>{product.stock_quantity}</dd>
              </div>
              <div>
                <dt>Image file</dt>
                <dd>{product.image_filename || "Not assigned"}</dd>
              </div>
            </dl>
          </article>

          <form className="panel form-grid" onSubmit={handleSubmit}>
            <h2>Create order</h2>
            <label>
              Quantity
              <input
                type="number"
                min="1"
                value={orderForm.quantity}
                onChange={(event) => setOrderForm({ ...orderForm, quantity: event.target.value })}
                required
              />
            </label>
            <label>
              Delivery address
              <input
                value={orderForm.address}
                onChange={(event) => setOrderForm({ ...orderForm, address: event.target.value })}
                required
              />
            </label>
            <label>
              Guest name
              <input
                value={orderForm.guest_name}
                onChange={(event) => setOrderForm({ ...orderForm, guest_name: event.target.value })}
              />
            </label>
            <label>
              Guest contact
              <input
                value={orderForm.guest_contact}
                onChange={(event) => setOrderForm({ ...orderForm, guest_contact: event.target.value })}
              />
            </label>
            <button className="button button--primary" type="submit">
              Submit order
            </button>
            <StatusBox tone={tone} message={status} />
          </form>
        </div>
      )}
    </section>
  );
}
