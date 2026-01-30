import { api } from "../api/api";

interface UploadDocumentParams {
  decisionId: number;
  file: File;
}

interface UploadResponse {
  filename: string;
  status: string;
  linked_to_decision: number;
}

export const uploadDocument = async ({
  decisionId,
  file,
}: UploadDocumentParams) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post<UploadResponse>(
    `/documents/upload`,
    formData,
    {
      params: { decision_id: decisionId },
      headers: { "Content-Type": "multipart/form-data" },
    },
  );
  return response.data;
};
