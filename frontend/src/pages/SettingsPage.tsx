export function SettingsPage() {
  return (
    <div className="grid gap-4 lg:grid-cols-2">
      {[
        ["LLM runtime", "llama.cpp, CPU threads only"],
        ["Speech runtime", "whisper.cpp with local model files"],
        ["OCR runtime", "PaddleOCR CPU with OpenCV preprocessing"],
        ["Database", "SQLite at backend/localintel.db"]
      ].map(([label, value]) => (
        <div key={label} className="glass rounded-lg p-5 shadow-glass">
          <div className="text-sm text-slate-500">{label}</div>
          <div className="mt-2 text-lg font-semibold">{value}</div>
        </div>
      ))}
      <div className="glass rounded-lg p-5 shadow-glass lg:col-span-2">
        <h2 className="text-xl font-semibold">Exports</h2>
        <div className="mt-4 flex flex-wrap gap-3">
          <a className="rounded-lg bg-slate-950 px-4 py-2 text-white dark:bg-emerald-400 dark:text-slate-950" href="/api/export/json">
            Download JSON
          </a>
          <a className="rounded-lg border border-slate-300 px-4 py-2 dark:border-slate-700" href="/api/export/csv">
            Download CSV
          </a>
        </div>
      </div>
    </div>
  );
}
