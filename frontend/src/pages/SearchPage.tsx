import { Search } from "lucide-react";
import { FormEvent, useState } from "react";

import { JsonViewer } from "../components/JsonViewer";
import { DocumentRecord, searchDocuments } from "../services/api";

export function SearchPage() {
  const [results, setResults] = useState<DocumentRecord[]>([]);
  const [query, setQuery] = useState({ keyword: "", entity: "", title: "", category: "", date: "" });

  async function submit(event: FormEvent) {
    event.preventDefault();
    const params = Object.fromEntries(Object.entries(query).filter(([, value]) => value));
    setResults(await searchDocuments(params));
  }

  return (
    <div className="grid gap-6 xl:grid-cols-[420px_1fr]">
      <form onSubmit={submit} className="glass rounded-lg p-5 shadow-glass">
        <h2 className="mb-4 text-xl font-semibold">Search</h2>
        {Object.keys(query).map((key) => (
          <label key={key} className="mb-3 block">
            <span className="mb-1 block text-sm capitalize text-slate-500">{key}</span>
            <input
              className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 dark:border-slate-700 dark:bg-slate-900"
              value={query[key as keyof typeof query]}
              onChange={(event) => setQuery((current) => ({ ...current, [key]: event.target.value }))}
            />
          </label>
        ))}
        <button className="mt-2 flex w-full items-center justify-center gap-2 rounded-lg bg-slate-950 px-4 py-3 text-white dark:bg-emerald-400 dark:text-slate-950">
          <Search size={18} /> Search records
        </button>
      </form>
      <div className="space-y-4">
        {results.map((item) => (
          <div key={item.id} className="glass rounded-lg p-5 shadow-glass">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <h3 className="text-lg font-semibold">{item.title}</h3>
                <p className="mt-1 text-sm text-slate-500">{item.summary}</p>
              </div>
              <span className="rounded-lg bg-emerald-500 px-3 py-1 text-sm text-slate-950">{item.priority}</span>
            </div>
            <div className="mt-4">
              <JsonViewer value={item} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
