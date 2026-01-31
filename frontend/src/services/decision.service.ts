import { api } from "../api/api";

interface DecisionResult {
  decision_id: number;
  ranked_options: Array<{
    option_id: number;
    score: number;
    reasons: string[];
  }>;
  consultant_report: string;
}

export const createDecision = async (title: string) => {
  const response = await api.post("/decisions", { title });
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
