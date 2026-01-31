import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { useDecisionResult } from "../hooks/useDecision"; // Adjust path if needed
import {
  Play,
  Loader2,
  Trophy,
  FileText,
  AlertTriangle,
  CheckCircle2,
} from "lucide-react";

interface DecisionResultProps {
  decisionId: number;
}

export default function DecisionResult({ decisionId }: DecisionResultProps) {
  const {
    data: result,
    isLoading,
    isError,
    refetch,
  } = useDecisionResult(decisionId, false);

  const [hasRun, setHasRun] = useState(false);

  const handleRun = () => {
    setHasRun(true);
    refetch();
  };

  const sortReasons = (reasons: string[]) => {
    return [...reasons].sort((a, b) => {
      const isGeminiA = a.startsWith("GEMINI");
      const isGeminiB = b.startsWith("GEMINI");
      if (isGeminiA && !isGeminiB) return -1;
      if (!isGeminiA && isGeminiB) return 1;
      return 0;
    });
  };

  return (
    <div className="w-full space-y-6">
      <div className="flex items-center justify-between p-4 bg-white border shadow-sm rounded-xl border-slate-200">
        <div>
          <h2 className="text-lg font-bold text-slate-800">Analysis Engine</h2>
          <p className="text-sm text-slate-500">
            {hasRun
              ? "Analysis complete based on uploaded evidence."
              : "Ready to process documents and generate strategy."}
          </p>
        </div>

        <button
          onClick={handleRun}
          disabled={isLoading}
          className={`flex items-center gap-2 px-6 py-3 font-bold text-white rounded-lg transition-all
            ${
              isLoading
                ? "bg-slate-400 cursor-not-allowed"
                : "bg-indigo-600 hover:bg-indigo-700 hover:shadow-md active:scale-95"
            }
          `}
        >
          {isLoading ? (
            <>
              <Loader2 className="animate-spin" size={20} />
              Running Engine...
            </>
          ) : (
            <>
              <Play size={20} fill="currentColor" />
              {hasRun ? "Re-run Analysis" : "Run Analysis"}
            </>
          )}
        </button>
      </div>

      {isError && (
        <div className="p-4 text-red-700 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2">
          <AlertTriangle size={20} />
          <span>Failed to fetch analysis. Please try again.</span>
        </div>
      )}

      {result && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="lg:col-span-1 space-y-4">
            <h3 className="font-semibold text-slate-700 flex items-center gap-2">
              <Trophy className="text-yellow-500" size={18} />
              Ranked Options
            </h3>

            <div className="space-y-3">
              {result.ranked_options.map((option, idx) => {
                const isWinner = idx === 0;
                return (
                  <div
                    key={option.option_id}
                    className={`p-4 rounded-xl border transition-all ${
                      isWinner
                        ? "bg-green-50 border-green-200 shadow-sm ring-1 ring-green-100"
                        : "bg-white border-slate-200 opacity-80"
                    }`}
                  >
                    <div className="flex justify-between items-center mb-2">
                      <span
                        className={`font-bold ${isWinner ? "text-green-800" : "text-slate-700"}`}
                      >
                        {idx + 1}. Option {option.option_id}
                      </span>
                      <span className="font-mono text-xl font-bold text-slate-900">
                        {option.score.toFixed(2)}
                      </span>
                    </div>

                    {/* Evidence List */}
                    <div className="space-y-1">
                      {sortReasons(option.reasons)
                        .slice(0, 4)
                        .map((reason, rIdx) => (
                          <div
                            key={rIdx}
                            className="text-xs text-slate-500 truncate flex items-start gap-1"
                          >
                            <CheckCircle2
                              size={12}
                              className="mt-0.5 text-slate-400 shrink-0"
                            />
                            <span title={reason}>
                              {reason
                                .replace("GEMINI:", "")
                                .replace("SUPPORTS:", "")
                                .trim()}
                            </span>
                          </div>
                        ))}
                      {option.reasons.length > 4 && (
                        <p className="text-xs text-slate-400 italic pl-4">
                          + {option.reasons.length - 4} more factors
                        </p>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Right Col: The Consultant Report */}
          <div className="lg:col-span-2">
            <h3 className="font-semibold text-slate-700 flex items-center gap-2 mb-4">
              <FileText className="text-indigo-500" size={18} />
              Strategic Directive
            </h3>

            <div className="bg-white border border-slate-200 rounded-xl p-8 shadow-sm min-h-[500px]">
              <article className="prose prose-indigo prose-sm sm:prose-base max-w-none">
                {/* Ensure consultant_report exists before rendering */}
                {result.consultant_report ? (
                  <ReactMarkdown>{result.consultant_report}</ReactMarkdown>
                ) : (
                  <div className="text-slate-400 italic text-center mt-20">
                    Report generation pending...
                  </div>
                )}
              </article>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
