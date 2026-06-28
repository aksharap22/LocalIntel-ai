import { BarChart3, Clock, Database, Home, Info, Moon, Search, Settings, Sun, Upload } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

const nav = [
  { to: "/", label: "Home", icon: Home },
  { to: "/dashboard", label: "Dashboard", icon: BarChart3 },
  { to: "/upload", label: "Upload", icon: Upload },
  { to: "/search", label: "Search", icon: Search },
  { to: "/history", label: "History", icon: Clock },
  { to: "/analytics", label: "Analytics", icon: Database },
  { to: "/settings", label: "Settings", icon: Settings },
  { to: "/about", label: "About", icon: Info }
];

interface LayoutProps {
  dark: boolean;
  onToggleTheme: () => void;
}

export function Layout({ dark, onToggleTheme }: LayoutProps) {
  return (
    <div className="min-h-screen bg-slate-100 text-slate-950 transition dark:bg-slate-950 dark:text-slate-100">
      <aside className="fixed left-0 top-0 z-20 hidden h-screen w-72 border-r border-slate-200/60 bg-white/80 p-4 backdrop-blur-xl dark:border-slate-800 dark:bg-slate-950/80 lg:block">
        <div className="mb-8 flex items-center gap-3 px-2">
          <div className="grid h-11 w-11 place-items-center rounded-lg bg-emerald-500 text-lg font-black text-slate-950">LI</div>
          <div>
            <div className="font-semibold">LocalIntel AI</div>
            <div className="text-xs text-slate-500">Offline CPU intelligence</div>
          </div>
        </div>
        <nav className="space-y-1">
          {nav.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition ${
                    isActive
                      ? "bg-slate-950 text-white dark:bg-emerald-400 dark:text-slate-950"
                      : "text-slate-600 hover:bg-slate-200/70 dark:text-slate-300 dark:hover:bg-slate-800"
                  }`
                }
              >
                <Icon size={18} />
                {item.label}
              </NavLink>
            );
          })}
        </nav>
      </aside>
      <main className="lg:pl-72">
        <header className="sticky top-0 z-10 border-b border-slate-200/70 bg-slate-100/80 px-4 py-3 backdrop-blur-xl dark:border-slate-800 dark:bg-slate-950/80">
          <div className="mx-auto flex max-w-7xl items-center justify-between">
            <div>
              <div className="text-sm text-slate-500">CPU-only local inference</div>
              <h1 className="text-xl font-semibold">LocalIntel AI</h1>
            </div>
            <button
              onClick={onToggleTheme}
              className="grid h-10 w-10 place-items-center rounded-lg border border-slate-300 bg-white text-slate-700 shadow-sm dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100"
              title="Toggle theme"
            >
              {dark ? <Sun size={18} /> : <Moon size={18} />}
            </button>
          </div>
        </header>
        <div className="mx-auto max-w-7xl p-4 sm:p-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
