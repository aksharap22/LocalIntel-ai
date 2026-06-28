import { useEffect, useState } from "react";

import { JsonViewer } from "../components/JsonViewer";
import { Analytics, fetchAnalytics } from "../services/api";

export function AnalyticsPage() {
  const [analytics, setAnalytics] = useState<Analytics | null>(null);

  useEffect(() => {
    fetchAnalytics().then(setAnalytics).catch(() => undefined);
  }, []);

  return (
    <div className="space-y-5">
      <div className="glass rounded-lg p-5 shadow-glass">
        <h2 className="text-xl font-semibold">Analytics</h2>
        <p className="mt-2 text-slate-500">Operational statistics generated from local SQLite records.</p>
      </div>
      <JsonViewer value={analytics ?? {}} />
    </div>
  );
}
