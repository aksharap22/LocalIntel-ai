import { FileAudio, FileText, Image, Timer } from "lucide-react";
import { useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { StatCard } from "../components/StatCard";
import { Analytics, fetchAnalytics } from "../services/api";

export function Dashboard() {
  const [analytics, setAnalytics] = useState<Analytics | null>(null);

  useEffect(() => {
    fetchAnalytics().then(setAnalytics).catch(() => undefined);
  }, []);

  const chartData = analytics
    ? Object.entries(analytics.by_type).map(([name, value]) => ({ name, value }))
    : [];

  return (
    <div className="space-y-6">
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard icon={FileText} label="Total Files" value={analytics?.total_files ?? 0} />
        <StatCard icon={FileText} label="Documents" value={analytics?.documents ?? 0} />
        <StatCard icon={Image} label="Images" value={analytics?.images ?? 0} />
        <StatCard icon={FileAudio} label="Audio" value={analytics?.audio ?? 0} />
      </div>
      <div className="grid gap-4 xl:grid-cols-[1fr_380px]">
        <section className="glass rounded-lg p-5 shadow-glass">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold">File Mix</h2>
            <Timer size={18} className="text-slate-500" />
          </div>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="value" fill="#22c55e" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>
        <section className="glass rounded-lg p-5 shadow-glass">
          <h2 className="mb-4 text-lg font-semibold">Latest Uploads</h2>
          <div className="space-y-3">
            {(analytics?.latest_uploads ?? []).map((item) => (
              <div key={item.id} className="rounded-lg border border-slate-200 p-3 dark:border-slate-800">
                <div className="font-medium">{item.title}</div>
                <div className="text-sm text-slate-500">{item.filename}</div>
              </div>
            ))}
          </div>
          <div className="mt-5 rounded-lg bg-slate-950 p-4 text-white dark:bg-slate-900">
            <div className="text-sm text-slate-400">Avg processing</div>
            <div className="text-2xl font-semibold">{Math.round(analytics?.average_processing_time_ms ?? 0)} ms</div>
          </div>
        </section>
      </div>
    </div>
  );
}
