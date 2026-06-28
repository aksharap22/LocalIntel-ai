export function AboutPage() {
  return (
    <div className="glass rounded-lg p-6 shadow-glass">
      <h2 className="text-2xl font-semibold">About LocalIntel AI</h2>
      <p className="mt-4 max-w-3xl text-slate-600 dark:text-slate-300">
        LocalIntel AI is an open-source offline intelligence platform. It extracts text from documents, scans, images,
        audio, and plain text, then structures the result as searchable JSON using local CPU-compatible inference
        runtimes.
      </p>
      <div className="mt-6 grid gap-3 sm:grid-cols-2">
        {["No cloud APIs", "SQLite persistence", "PWA shell", "JSON and CSV export"].map((item) => (
          <div key={item} className="rounded-lg border border-slate-200 p-4 dark:border-slate-800">
            {item}
          </div>
        ))}
      </div>
    </div>
  );
}
