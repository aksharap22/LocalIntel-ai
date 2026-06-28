import { useEffect, useState } from "react";
import { Route, Routes } from "react-router-dom";

import { Layout } from "./components/Layout";
import { AboutPage } from "./pages/AboutPage";
import { AnalyticsPage } from "./pages/AnalyticsPage";
import { Dashboard } from "./pages/Dashboard";
import { HistoryPage } from "./pages/HistoryPage";
import { Home } from "./pages/Home";
import { SearchPage } from "./pages/SearchPage";
import { SettingsPage } from "./pages/SettingsPage";
import { UploadPage } from "./pages/UploadPage";

export default function App() {
  const [dark, setDark] = useState(() => localStorage.getItem("theme") !== "light");

  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
    localStorage.setItem("theme", dark ? "dark" : "light");
  }, [dark]);

  return (
    <Routes>
      <Route element={<Layout dark={dark} onToggleTheme={() => setDark((value) => !value)} />}>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/about" element={<AboutPage />} />
      </Route>
    </Routes>
  );
}
