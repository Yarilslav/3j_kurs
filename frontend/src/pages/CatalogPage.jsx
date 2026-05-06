import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import { fetchProducts } from "../api/products";
import StatusBox from "../components/StatusBox";

export default function CatalogPage() {
  const [products, setProducts] = useState([]);
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("");

  useEffect(() => {
    async function loadProducts() {
      try {
        const result = await fetchProducts();
        setProducts(result);
      } catch (error) {
        setStatus(error.message);
      }
    }

    loadProducts();
  }, []);

  const filteredProducts = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    if (!normalized) {
      return products;
    }
    return products.filter((product) =>
      [product.name, product.native_name, product.kind, ...(product.categories || [])]
        .filter(Boolean)
        .some((value) => value.toLowerCase().includes(normalized)),
    );
  }, [products, query]);

  return (
    <section className="stack-large">
      <div className="page-header">
        <span className="eyebrow">Route /catalog</span>
        <h1>Tea catalog</h1>
        <p>Live product cards from the FastAPI backend with a simple placeholder filter.</p>
      </div>

      <div className="panel toolbar">
        <label className="toolbar__search">
          Search / filter
          <input
            placeholder="green, oolong, iron goddess..."
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
        </label>
        <div className="toolbar__meta">
          <strong>{filteredProducts.length}</strong>
          <span>visible products</span>
        </div>
      </div>

      <StatusBox tone="warning" message={status} />

      <div className="catalog-grid">
        {filteredProducts.map((product) => (
          <article key={product.id} className="panel product-card">
            <div className="product-card__meta">
              <span className="eyebrow">#{product.id}</span>
              <h2>{product.name}</h2>
              <p>{product.native_name || "Native name not provided"}</p>
            </div>
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
                <dt>In stock</dt>
                <dd>{product.stock_quantity}</dd>
              </div>
            </dl>
            <Link className="button button--primary" to={`/catalog/${product.id}`}>
              Open product
            </Link>
          </article>
        ))}
      </div>
    </section>
  );
}
