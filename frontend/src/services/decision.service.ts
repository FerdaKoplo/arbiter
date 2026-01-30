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

interface DecisionResult {
  data: {
    decision_id: number;
    ranked_options: Array<{
      option_id: number;
      score: number;
      reasons: string[];
    }>;
  };
  consultant_report: string;
}

export const createDecision = async (title: string) => {
  const response = await api.post("/decisions", { title });
  return response.data;
};

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

export const getDecisionResult = async (
  decisionId: number,
): Promise<DecisionResult> => {
  const response = await api.get<DecisionResult>(
    `/decisions/${decisionId}/evaluate`,
  );
  return response.data;
};
