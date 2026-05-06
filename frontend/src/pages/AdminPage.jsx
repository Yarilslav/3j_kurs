import { useEffect, useState } from "react";

import { createProduct, deleteProduct, fetchProducts, updateProduct } from "../api/products";
import StatusBox from "../components/StatusBox";

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
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState(initialProduct);
  const [editingId, setEditingId] = useState(null);
  const [status, setStatus] = useState("");
  const [tone, setTone] = useState("neutral");

  async function loadProducts() {
    try {
      const result = await fetchProducts();
      setProducts(result);
    } catch (error) {
      setTone("warning");
      setStatus(error.message);
    }
  }

  useEffect(() => {
    loadProducts();
  }, []);

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

  async function handleDelete(productId) {
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

  return (
    <section className="stack-large">
      <div className="page-header">
        <span className="eyebrow">Route /admin</span>
        <h1>Admin product panel</h1>
        <p>Demonstration staff/admin page for product create, edit, and delete operations.</p>
      </div>

      <StatusBox tone={tone} message={status} />

      <div className="two-column two-column--wide">
        <form className="panel form-grid" onSubmit={handleSubmit}>
          <h2>{editingId ? `Edit product #${editingId}` : "Create product"}</h2>
          <label>
            Name
            <input value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} required />
          </label>
          <label>
            Native name
            <input value={form.native_name} onChange={(event) => setForm({ ...form, native_name: event.target.value })} />
          </label>
          <label>
            Image filename
            <input value={form.image_filename} onChange={(event) => setForm({ ...form, image_filename: event.target.value })} />
          </label>
          <label>
            Kind
            <input value={form.kind} onChange={(event) => setForm({ ...form, kind: event.target.value })} required />
          </label>
          <label>
            Categories
            <input value={form.categories} onChange={(event) => setForm({ ...form, categories: event.target.value })} required />
          </label>
          <label>
            Description
            <textarea value={form.description} onChange={(event) => setForm({ ...form, description: event.target.value })} rows="4" />
          </label>
          <label>
            Price UAH
            <input type="number" min="0" value={form.price_uah} onChange={(event) => setForm({ ...form, price_uah: event.target.value })} required />
          </label>
          <label>
            Stock quantity
            <input type="number" min="0" value={form.stock_quantity} onChange={(event) => setForm({ ...form, stock_quantity: event.target.value })} required />
          </label>
          <div className="button-row">
            <button className="button button--primary" type="submit">
              {editingId ? "Save changes" : "Create product"}
            </button>
            <button
              className="button"
              type="button"
              onClick={() => {
                setEditingId(null);
                setForm(initialProduct);
              }}
            >
              Clear
            </button>
          </div>
        </form>

        <div className="panel stack-medium">
          <h2>Current product list</h2>
          {products.map((product) => (
            <article key={product.id} className="admin-product-row">
              <div>
                <strong>{product.name}</strong>
                <p>{product.kind} · {product.price_uah} UAH</p>
              </div>
              <div className="button-row">
                <button className="button" type="button" onClick={() => startEdit(product)}>
                  Edit
                </button>
                <button className="button button--danger" type="button" onClick={() => handleDelete(product.id)}>
                  Delete
                </button>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
