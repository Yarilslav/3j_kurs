import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Home" },
  { to: "/auth", label: "Auth" },
  { to: "/catalog", label: "Catalog" },
  { to: "/booking", label: "Booking" },
  { to: "/admin", label: "Admin" },
];

export default function NavBar() {
  return (
    <nav className="nav-shell">
      <div className="brand-mark">
        <span className="brand-mark__eyebrow">Tea House</span>
        <strong>Asahi</strong>
      </div>
      <div className="nav-links">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) => (isActive ? "nav-link nav-link--active" : "nav-link")}
          >
            {link.label}
          </NavLink>
        ))}
      </div>
    </nav>
  );
}
