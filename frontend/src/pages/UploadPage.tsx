import { FileUp, Loader2 } from "lucide-react";
import { DragEvent, useState } from "react";

import { JsonViewer } from "../components/JsonViewer";
import { DocumentRecord, processFile, uploadFile } from "../services/api";

const stages = ["Upload", "Extract", "Infer", "Persist"];

export function UploadPage() {
  const [progress, setProgress] = useState(0);
  const [stage, setStage] = useState("Idle");
  const [record, setRecord] = useState<DocumentRecord | null>(null);
  const [error, setError] = useState("");

  async function handleFiles(files: FileList | null) {
    const file = files?.[0];
    if (!file) return;
    setError("");
    setRecord(null);
    try {
      setStage("Upload");
      const uploaded = await uploadFile(file, setProgress);
      setStage("Extract");
      const processed = await processFile(uploaded.id);
      setStage("Persist");
      setRecord(processed);
      setStage("Complete");
    /* eslint-disable-next-line @typescript-eslint/no-explicit-any */
    } catch (exc: any) {
      if (import.meta.env.DEV) {
        console.error("Full error:", exc);
        console.error("Response:", exc.response);
        console.error("Data:", exc.response?.data);
      }

      setError(
        JSON.stringify(exc.response?.data, null, 2) ||
        exc.message ||
        "Upload failed"
      );

      setStage("Error");
    }
  }

  function drop(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault();
    handleFiles(event.dataTransfer.files);
  }

  return (
    <div className="grid gap-6 xl:grid-cols-[0.8fr_1.2fr]">
      <section className="glass rounded-lg p-6 shadow-glass">
        <h2 className="mb-4 text-xl font-semibold">Upload</h2>
        <label
          onDragOver={(event) => event.preventDefault()}
          onDrop={drop}
          className="flex min-h-72 cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-slate-300 p-8 text-center transition hover:border-emerald-400 dark:border-slate-700"
        >
          <FileUp size={42} className="mb-4 text-emerald-500" />
          <span className="text-lg font-medium">Drop files here</span>
          <span className="mt-2 text-sm text-slate-500">PDF, DOCX, PNG, JPG, JPEG, WAV, MP3, TXT</span>
          <input type="file" className="hidden" onChange={(event) => handleFiles(event.target.files)} />
        </label>
        <div className="mt-5">
          <div className="mb-2 flex items-center justify-between text-sm">
            <span>{stage}</span>
            <span>{progress}%</span>
          </div>
          <div className="h-2 overflow-hidden rounded-full bg-slate-200 dark:bg-slate-800">
            <div className="h-full bg-emerald-500 transition-all" style={{ width: `${progress}%` }} />
          </div>
        </div>
        <div className="mt-5 grid grid-cols-4 gap-2">
          {stages.map((item) => (
            <div
              key={item}
              className={`rounded-lg p-2 text-center text-xs ${
                item === stage || stage === "Complete" ? "bg-emerald-500 text-slate-950" : "bg-slate-200 dark:bg-slate-800"
              }`}
            >
              {item}
            </div>
          ))}
        </div>
        {stage !== "Idle" && stage !== "Complete" && stage !== "Error" ? (
          <div className="mt-4 flex items-center gap-2 text-sm text-slate-500">
            <Loader2 className="animate-spin" size={16} /> Processing locally
          </div>
        ) : null}
        {error ? <div className="mt-4 rounded-lg bg-red-500/10 p-3 text-sm text-red-600">{error}</div> : null}
      </section>
      <section>{record ? <JsonViewer value={record} /> : <div className="glass rounded-lg p-6 text-slate-500 shadow-glass">Processed JSON appears here.</div>}</section>
    </div>
  );
}
