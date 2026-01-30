import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  createDecision,
  getDecisionResult,
} from "../services/decision.service";
import { uploadDocument } from "../services/document.service";

export const decisionKeys = {
  all: ["decisions"] as const,
  detail: (id: number) => ["decision", id] as const,
};

export const useCreateDecision = () => {
  return useMutation({
    mutationFn: createDecision,
  });
};

export const useUploadDocument = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: uploadDocument,
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({
        queryKey: decisionKeys.detail(variables.decisionId),
      });
    },
  });
};

export const useDecisionResult = (
  decisionId: number,
  enabled: boolean = false,
) => {
  return useQuery({
    queryKey: decisionKeys.detail(decisionId),
    queryFn: () => getDecisionResult(decisionId),
    enabled: enabled,
    staleTime: 0,
    retry: false,
  });
};
