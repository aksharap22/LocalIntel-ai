import { Check, Copy } from "lucide-react";
import { useState } from "react";

export function JsonViewer({ value }: { value: unknown }) {
  const [copied, setCopied] = useState(false);
  const json = JSON.stringify(value, null, 2);

  async function copy() {
    await navigator.clipboard.writeText(json);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1400);
  }

  return (
    <div className="overflow-hidden rounded-lg border border-slate-200 bg-slate-950 text-slate-100 dark:border-slate-800">
      <div className="flex items-center justify-between border-b border-slate-800 px-4 py-2">
        <span className="text-xs uppercase tracking-wide text-slate-400">JSON</span>
        <button onClick={copy} className="grid h-8 w-8 place-items-center rounded-md hover:bg-slate-800" title="Copy JSON">
          {copied ? <Check size={16} /> : <Copy size={16} />}
        </button>
      </div>
      <pre className="max-h-[520px] overflow-auto p-4 text-sm leading-6">
        <code>{json}</code>
      </pre>
    </div>
  );
}
