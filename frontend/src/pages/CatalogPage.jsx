import { useEffect, useMemo, useState } from "react";
import { Link, useOutletContext } from "react-router-dom";

import { fetchProducts } from "../api/products";
import StatusBox from "../components/StatusBox";
import { addItemToDraft, loadOrderDraft, saveOrderDraft } from "../utils/orderDraft";
import { getProductImage } from "../utils/productAssets";

export default function CatalogPage() {
  const { currentUser } = useOutletContext();
  const [products, setProducts] = useState([]);
  const [query, setQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [status, setStatus] = useState("");
  const [tone, setTone] = useState("neutral");

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

  const categories = useMemo(
    () =>
      Array.from(
        new Set(products.flatMap((product) => product.categories || []).filter(Boolean)),
      ),
    [products],
  );

  function handleAddToDraft(productId) {
    const accountKey = currentUser?.login || "guest";
    const nextDraft = addItemToDraft(loadOrderDraft(accountKey), productId);
    saveOrderDraft(accountKey, nextDraft);
    setTone("success");
    setStatus("Товар додано до формування замовлення.");
  }

  const filteredProducts = products.filter((product) => {
    const normalized = query.trim().toLowerCase();
    const matchesQuery =
      !normalized ||
      [product.name, product.native_name, product.kind, ...(product.categories || [])]
        .filter(Boolean)
        .some((value) => value.toLowerCase().includes(normalized));
    const matchesCategory =
      selectedCategory === "all" || (product.categories || []).includes(selectedCategory);
    return matchesQuery && matchesCategory;
  });

  return (
    <section className="page-stack">
      <div className="section-card__header">
        <h1>Каталог товарів</h1>
      </div>

      <div className="catalog-layout">
        <aside className="filter-scroll">
          <div className="filter-scroll__rod" />
          <div className="filter-scroll__body">
            <p className="filter-scroll__lead">Знайдіть саме те, що вам потрібно</p>
            <label className="form-grid">
              <span>Пошук</span>
              <input
                placeholder="зелений, улун, колекція..."
                value={query}
                onChange={(event) => setQuery(event.target.value)}
              />
            </label>

            <div className="filter-group">
              <span className="filter-group__label">Категорії</span>
              <button
                type="button"
                className={selectedCategory === "all" ? "filter-chip filter-chip--active" : "filter-chip"}
                onClick={() => setSelectedCategory("all")}
              >
                Усе
              </button>
              {categories.map((category) => (
                <button
                  key={category}
                  type="button"
                  className={selectedCategory === category ? "filter-chip filter-chip--active" : "filter-chip"}
                  onClick={() => setSelectedCategory(category)}
                >
                  {category}
                </button>
              ))}
            </div>

            <div className="filter-scroll__meta">
              <strong>{filteredProducts.length}</strong>
              <span>позицій видно зараз</span>
            </div>
          </div>
        </aside>

        <div className="catalog-main">
          <StatusBox tone={tone} message={status} />

          <div className="catalog-grid">
            {filteredProducts.map((product) => (
              <article key={product.id} className="tea-card">
                <div className="tea-card__visual">
                  {getProductImage(product) ? (
                    <img src={getProductImage(product)} alt={product.name} />
                  ) : (
                    <span>Картинка</span>
                  )}
                </div>
                <div className="tea-card__body">
                  <div className="tea-card__header">
                    <Link className="tea-card__title" to={`/catalog/${product.id}`}>
                      {product.name}
                    </Link>
                    <p>{product.native_name || "Назва мовою оригіналу ще не додана"}</p>
                  </div>

                  <div className="tea-card__meta">
                    <span>{product.stock_quantity > 0 ? "Наявність" : "Немає в наявності"}</span>
                    <span>Ціна/50г</span>
                  </div>
                  <div className="tea-card__meta tea-card__meta--values">
                    <strong>{product.stock_quantity > 0 ? `${product.stock_quantity} шт.` : "Очікується"}</strong>
                    <strong>{product.price_uah} грн</strong>
                  </div>
                </div>

                <div className="tea-card__actions">
                  <Link className="button button--ghost" to={`/catalog/${product.id}`}>
                    Детальніше
                  </Link>
                  <button
                    className="button button--soft-accent"
                    type="button"
                    onClick={() => handleAddToDraft(product.id)}
                  >
                    Додати...
                  </button>
                </div>
              </article>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
