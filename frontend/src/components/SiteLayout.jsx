import { Outlet } from "react-router-dom";

import NavBar from "./NavBar";

export default function SiteLayout() {
  return (
    <div className="page-shell">
      <NavBar />
      <main className="content-shell">
        <Outlet />
      </main>
    </div>
  );
}
