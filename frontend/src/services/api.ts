import axios from "axios";

export interface DocumentRecord {
  id: string;
  filename: string;
  type: string;
  title: string;
  summary: string;
  entities: string[];
  keywords: string[];
  priority: string;
  confidence: number;
  metadata: Record<string, unknown>;
  status: string;
  created_at: string;
  processed_at?: string;
  processing_time_ms?: number;
}

export interface Analytics {
  total_files: number;
  documents: number;
  images: number;
  audio: number;
  average_processing_time_ms: number;
  latest_uploads: DocumentRecord[];
  by_type: Record<string, number>;
  by_priority: Record<string, number>;
}

// Read backend URL from .env (set VITE_API_URL in .env for production).
// Local dev falls back to the Vite proxy at /api, which forwards to the
// FastAPI backend on port 8000 — see vite.config.ts.
const API_URL = import.meta.env.VITE_API_URL || "/api";

if (import.meta.env.DEV) {
  console.log("Backend URL:", API_URL);
}

export const api = axios.create({
  baseURL: API_URL,
  timeout: 600000,
});

export async function fetchDocuments() {
  const { data } = await api.get<DocumentRecord[]>("/documents");
  return data;
}

export async function fetchAnalytics() {
  const { data } = await api.get<Analytics>("/analytics");
  return data;
}

export async function uploadFile(
  file: File,
  onProgress: (progress: number) => void
) {
  const form = new FormData();
  form.append("file", file);

  try {
    if (import.meta.env.DEV) console.log("Uploading:", file.name);

    // Do NOT set Content-Type here — axios must add the multipart boundary
    // itself. Without the boundary parameter, FastAPI's multipart parser
    // returns 400.
    const { data } = await api.post<{
      id: string;
      filename: string;
      type: string;
      status: string;
    }>("/upload", form, {
      onUploadProgress: (event) => {
        if (event.total) {
          onProgress(Math.round((event.loaded / event.total) * 100));
        }
      },
    });

    if (import.meta.env.DEV) console.log("UPLOAD SUCCESS:", data);
    return data;
  /* eslint-disable-next-line @typescript-eslint/no-explicit-any */
  } catch (error: any) {
    if (import.meta.env.DEV) {
      console.error("UPLOAD ERROR", error, error?.response);
    }
    throw error;
  }
}

export async function processFile(id: string) {
  try {
    if (import.meta.env.DEV) console.log("Processing document:", id);

    const { data } = await api.post<DocumentRecord>("/process", null, {
      params: { id },
    });

    if (import.meta.env.DEV) console.log("PROCESS SUCCESS:", data);
    return data;
  /* eslint-disable-next-line @typescript-eslint/no-explicit-any */
  } catch (error: any) {
    if (import.meta.env.DEV) {
      console.error("PROCESS ERROR", error, error?.response);
    }
    throw error;
  }
}

export async function searchDocuments(params: Record<string, string>) {
  const { data } = await api.get<DocumentRecord[]>("/search", {
    params,
  });
  return data;
}

export async function fetchDocument(id: string) {
  const { data } = await api.get<DocumentRecord>(`/document/${id}`);
  return data;
}

export async function deleteDocument(id: string) {
  await api.delete(`/document/${id}`);
}

export async function exportJson() {
  const { data } = await api.get("/export/json");
  return data;
}

export async function exportCsv() {
  const response = await api.get("/export/csv", {
    responseType: "blob",
  });

  return response.data;
}

export async function healthCheck() {
  const { data } = await api.get("/health");
  return data;
}