import { Outlet } from "react-router-dom";
import { useEffect, useState } from "react";

import { fetchMe } from "../api/auth";
import NavBar from "./NavBar";

export default function SiteLayout() {
  const [currentUser, setCurrentUser] = useState(null);

  async function refreshCurrentUser() {
    try {
      const user = await fetchMe();
      setCurrentUser(user);
    } catch {
      setCurrentUser(null);
    }
  }

  useEffect(() => {
    refreshCurrentUser();
  }, []);

  return (
    <div className="page-shell">
      <NavBar currentUser={currentUser} />
      <main className="content-shell">
        <Outlet context={{ currentUser, refreshCurrentUser }} />
      </main>
    </div>
  );
}
