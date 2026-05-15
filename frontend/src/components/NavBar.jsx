import { NavLink, Link } from "react-router-dom";

import logoImage from "../assets/Icons/Asahi_logo1.png";
import teaIcon from "../assets/Icons/Iconka2_.png";
import orderIcon from "../assets/Icons/Iconka3_.png";
import bookingIcon from "../assets/Icons/Iconka4_.png";

const topLinks = [
  { label: "Про нас", to: "/" },
  { label: "Контакти", to: "/" },
  { label: "Доставка", to: "/" },
  { label: "Відгуки", to: "/" },
  { label: "Політика Конфіденційності", to: "/" },
];

const mainLinks = [
  { to: "/catalog", label: "Чай", icon: teaIcon },
  { to: "/order", label: "Зробити замовлення", icon: orderIcon, multiline: true },
  { to: "/booking", label: "Забронювати місця", icon: bookingIcon, multiline: true },
];

const socialLinks = [
  { label: "▶", className: "social-link social-link--youtube" },
  { label: "✈", className: "social-link social-link--telegram" },
  { label: "◎", className: "social-link social-link--instagram" },
  { label: "X", className: "social-link social-link--x" },
];

export default function NavBar({ currentUser }) {
  const showAdminLink = currentUser && ["admin", "staff"].includes(currentUser.role);

  return (
    <header className="header-shell">
      <div className="header-shell__top">
        <div className="social-links" aria-label="Соціальні мережі">
          {socialLinks.map((link) => (
            <button key={link.label} type="button" className={link.className} aria-label={link.label}>
              {link.label}
            </button>
          ))}
        </div>
        <div className="header-shell__top-links">
          {topLinks.map((link) => (
            <Link key={link.label} className="header-top-link" to={link.to}>
              {link.label}
            </Link>
          ))}
        </div>
      </div>

      <div className="header-shell__main">
        <Link className="brand-block" to="/">
          <img className="brand-block__logo" src={logoImage} alt="Asahi logo" />
        </Link>

        <nav className="main-nav" aria-label="Основна навігація">
          {mainLinks.map((link) => (
            <NavLink
              key={link.to + link.label}
              to={link.to}
              className={({ isActive }) => (isActive ? "main-nav__link main-nav__link--active" : "main-nav__link")}
            >
              <span className="main-nav__icon-shell">
                <img className="main-nav__icon" src={link.icon} alt="" />
              </span>
              <span className={link.multiline ? "main-nav__label main-nav__label--multiline" : "main-nav__label"}>
                {link.label}
              </span>
            </NavLink>
          ))}

          {showAdminLink ? (
            <NavLink
              to="/admin"
              className={({ isActive }) => (isActive ? "main-nav__link main-nav__link--active" : "main-nav__link")}
            >
              <span className="main-nav__icon-shell main-nav__icon-shell--admin">A</span>
              <span className="main-nav__label">Панель</span>
            </NavLink>
          ) : null}
        </nav>

        <NavLink className="auth-cta" to="/auth">
          {currentUser ? currentUser.login : "Увійти"}
        </NavLink>
      </div>
    </header>
  );
}
