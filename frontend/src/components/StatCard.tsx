import { LucideIcon } from "lucide-react";

export function StatCard({ label, value, icon: Icon }: { label: string; value: string | number; icon: LucideIcon }) {
  return (
    <div className="glass rounded-lg p-5 shadow-glass">
      <div className="flex items-start justify-between">
        <div>
          <div className="text-sm text-slate-500 dark:text-slate-400">{label}</div>
          <div className="mt-2 text-3xl font-semibold">{value}</div>
        </div>
        <div className="grid h-10 w-10 place-items-center rounded-lg bg-emerald-500 text-slate-950">
          <Icon size={20} />
        </div>
      </div>
    </div>
  );
}
