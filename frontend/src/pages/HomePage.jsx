import { Link } from "react-router-dom";

import { homeScenarios } from "../mock/homeScenarios";

export default function HomePage() {
  return (
    <section className="stack-large">
      <div className="hero-grid">
        <div className="panel panel--hero">
          <span className="eyebrow">Low-fi demo interface</span>
          <h1>Tea House Asahi</h1>
          <p>
            Minimal React showcase for the tea catalog, guest booking flow, and basic staff product
            management.
          </p>
          <div className="button-row">
            <Link className="button button--primary" to="/catalog">
              Open catalog
            </Link>
            <Link className="button" to="/booking">
              Book seats
            </Link>
          </div>
        </div>
        <div className="panel">
          <h2>Project intent</h2>
          <ul className="plain-list">
            <li>Show the main customer journeys.</li>
            <li>Connect React pages to the real FastAPI backend.</li>
            <li>Keep the interface intentionally low-fi and easy to explain.</li>
          </ul>
        </div>
      </div>

      <div className="panel">
        <h2>Scenario map</h2>
        <div className="scenario-grid">
          {homeScenarios.map((scenario) => (
            <article key={scenario.title} className="scenario-card">
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
