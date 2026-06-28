import { Link } from "react-router-dom";

export function Home() {
  return (
    <section className="grid min-h-[calc(100vh-130px)] content-center gap-8 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
      <div className="space-y-6">
        <div className="inline-flex rounded-lg border border-emerald-400/40 bg-emerald-400/10 px-3 py-1 text-sm text-emerald-700 dark:text-emerald-300">
          Offline-first. CPU-only. No cloud inference.
        </div>
        <h2 className="max-w-4xl text-5xl font-semibold leading-tight sm:text-6xl">LocalIntel AI</h2>
        <p className="max-w-2xl text-lg text-slate-600 dark:text-slate-300">
          Convert PDFs, images, audio, scanned documents, and plain text into structured JSON records using local
          inference runtimes on ordinary laptops.
        </p>
        <div className="flex flex-wrap gap-3">
          <Link to="/upload" className="rounded-lg bg-slate-950 px-5 py-3 text-white dark:bg-emerald-400 dark:text-slate-950">
            Upload files
          </Link>
          <Link to="/dashboard" className="rounded-lg border border-slate-300 px-5 py-3 dark:border-slate-700">
            View dashboard
          </Link>
        </div>
      </div>
      <div className="glass rounded-lg p-5 shadow-glass">
        <div className="grid gap-3">
          {["PyMuPDF extraction", "OpenCV preprocessing", "PaddleOCR CPU OCR", "whisper.cpp transcription", "llama.cpp JSON synthesis"].map(
            (stage, index) => (
              <div key={stage} className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-800">
                <span className="grid h-8 w-8 place-items-center rounded-md bg-emerald-500 text-sm font-bold text-slate-950">
                  {index + 1}
                </span>
                <span>{stage}</span>
              </div>
            )
          )}
        </div>
      </div>
    </section>
  );
}
