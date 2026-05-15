import { Link } from "react-router-dom";

import { homeScenarios } from "../mock/homeScenarios";

export default function HomePage() {
  return (
    <section className="page-stack">
      <div className="landing-hero">
        <div className="landing-hero__copy">
          <span className="eyebrow">Чайна атмосфера, жива навігація, новий вигляд</span>
          <h1>Asahi</h1>
          <p>
            Новий інтерфейс для каталогу, замовлень, бронювання і внутрішньої роботи персоналу.
          </p>
          <div className="hero-actions">
            <Link className="button button--primary" to="/catalog">
              Перейти до каталогу
            </Link>
            <Link className="button" to="/booking">
              Забронювати місця
            </Link>
          </div>
        </div>

        <div className="landing-hero__cards">
          <article className="feature-card">
            <span className="eyebrow">Каталог</span>
            <h2>Живі позиції з бази</h2>
            <p>Назви, категорії, ціни, наявність і короткий шлях до створення замовлення.</p>
          </article>
          <article className="feature-card">
            <span className="eyebrow">Бронювання</span>
            <h2>Той самий сценарій, але в новій обгортці</h2>
            <p>Форма бронювання і карта місць зібрані в спокійний, єдиний стиль.</p>
          </article>
        </div>
      </div>

      <div className="section-card">
        <div className="section-card__header">
          <span className="eyebrow">Сценарії</span>
          <h2>Що вже можна пройти у проєкті</h2>
        </div>
        <div className="scenario-grid">
          {homeScenarios.map((scenario) => (
            <article key={scenario.title} className="scenario-card scenario-card--soft">
              <h3>{scenario.title}</h3>
              <ol>
                {scenario.steps.map((step) => (
                  <li key={step}>{step}</li>
                ))}
              </ol>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
