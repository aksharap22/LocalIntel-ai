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

// Backend URL
const API_URL = "http://127.0.0.1:8000";

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

  const { data } = await api.post<{
    id: string;
    filename: string;
    type: string;
    status: string;
  }>("/upload", form, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
    onUploadProgress: (event) => {
      if (event.total) {
        onProgress(Math.round((event.loaded / event.total) * 100));
      }
    },
  });

  return data;
}

export async function processFile(id: string) {
  const { data } = await api.post<DocumentRecord>("/process", null, {
    params: {
      id,
    },
  });

  return data;
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