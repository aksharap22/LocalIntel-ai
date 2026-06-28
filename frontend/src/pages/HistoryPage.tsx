import { useEffect, useState } from "react";

import { DocumentRecord, fetchDocuments } from "../services/api";

export function HistoryPage() {
  const [documents, setDocuments] = useState<DocumentRecord[]>([]);

  useEffect(() => {
    fetchDocuments().then(setDocuments).catch(() => undefined);
  }, []);

  return (
    <div className="glass rounded-lg p-5 shadow-glass">
      <h2 className="mb-4 text-xl font-semibold">History</h2>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[720px] text-left text-sm">
          <thead className="text-slate-500">
            <tr>
              <th className="py-2">Filename</th>
              <th>Type</th>
              <th>Priority</th>
              <th>Confidence</th>
              <th>Created</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {documents.map((item) => (
              <tr key={item.id} className="border-t border-slate-200 dark:border-slate-800">
                <td className="py-3">{item.filename}</td>
                <td>{item.type}</td>
                <td>{item.priority}</td>
                <td>{Math.round(item.confidence * 100)}%</td>
                <td>{new Date(item.created_at).toLocaleString()}</td>
                <td>{item.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
