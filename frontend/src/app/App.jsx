import { Route, Routes } from "react-router-dom";

import SiteLayout from "../components/SiteLayout";
import AdminPage from "../pages/AdminPage";
import AuthPage from "../pages/AuthPage";
import BookingPage from "../pages/BookingPage";
import CatalogPage from "../pages/CatalogPage";
import HomePage from "../pages/HomePage";
import ProductPage from "../pages/ProductPage";

export default function App() {
  return (
    <Routes>
      <Route element={<SiteLayout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/auth" element={<AuthPage />} />
        <Route path="/catalog" element={<CatalogPage />} />
        <Route path="/catalog/:productId" element={<ProductPage />} />
        <Route path="/booking" element={<BookingPage />} />
        <Route path="/admin" element={<AdminPage />} />
      </Route>
    </Routes>
  );
}
