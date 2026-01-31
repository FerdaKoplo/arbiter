import { useState, type ComponentPropsWithoutRef } from "react";
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
import { MermaidChart } from "./MermaidChart";
import type { ExtraProps } from "react-markdown";

interface DecisionResultProps {
  decisionId: number;
}

type MarkdownHeaderProps = ComponentPropsWithoutRef<"h1"> & {
  node?: object;
};

type MarkdownCodeProps = ComponentPropsWithoutRef<"code"> & {
  inline?: boolean;
  node?: object;
};

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
    <div className="w-full space-y-8">
      {/* Top Engine Control - Glassmorphism Card */}
      <div className="relative flex items-center justify-between p-8 bg-white/40 backdrop-blur-3xl rounded-[2.5rem] border border-white/60 shadow-[0_20px_40px_-15px_rgba(0,0,0,0.2)] overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-[40%] bg-gradient-to-b from-white/50 to-transparent pointer-events-none" />

        <div className="relative z-10">
          <h2 className="text-2xl font-black text-white tracking-tight drop-shadow-sm uppercase">
            Analysis Engine
          </h2>
          <p className="text-white drop-shadow-sm font-bold text-sm">
            {hasRun
              ? "Analysis complete based on uploaded evidence."
              : "Ready to process documents and generate strategy."}
          </p>
        </div>

        <button
          onClick={handleRun}
          disabled={isLoading}
          className={`relative flex items-center gap-3 px-8 py-4 font-black text-white rounded-2xl transition-all overflow-hidden shadow-lg border-t border-white/50
            ${
              isLoading
                ? "bg-slate-400/20 cursor-not-allowed"
                : "bg-white/10 hover:bg-white/20 active:scale-95"
            }
          `}
        >
          {/* Button Gloss Sheen */}
          <div className="absolute top-0 left-0 w-full h-[45%] bg-gradient-to-b from-white/40 to-transparent pointer-events-none" />

          <span className="relative z-10 flex items-center gap-2">
            {isLoading ? (
              <>
                <Loader2 className="animate-spin" size={20} />
                Running Engine...
              </>
            ) : (
              <>
                <Play
                  size={20}
                  fill="currentColor"
                  className="drop-shadow-sm"
                />
                {hasRun ? "Re-run Analysis" : "Run Analysis"}
              </>
            )}
          </span>
        </button>
      </div>

      {isError && (
        <div className="p-4 text-red-900 font-bold bg-red-400/20 backdrop-blur-md border border-red-400/50 rounded-2xl flex items-center gap-2 shadow-inner">
          <AlertTriangle size={20} />
          <span>Failed to fetch analysis. Please try again.</span>
        </div>
      )}

      {result && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
          {/* Left Column: Ranked Options */}
          <div className="lg:col-span-1 space-y-6">
            <h3 className="font-black text-white uppercase tracking-widest text-xs flex items-center gap-2 ml-4 drop-shadow-md">
              <Trophy className="text-yellow-400 drop-shadow-sm" size={18} />
              Ranked Options
            </h3>

            <div className="space-y-4">
              {result.ranked_options.map((option, idx) => {
                const isWinner = idx === 0;
                return (
                  <div
                    key={option.option_id}
                    className={`relative p-6 rounded-[2rem] border transition-all overflow-hidden shadow-lg group ${
                      isWinner
                        ? "bg-white/55 border-white ring-4 ring-green-400/20"
                        : "bg-white/20 border-white/40"
                    }`}
                  >
                    <div className="absolute top-0 left-0 w-full h-[40%] bg-gradient-to-b from-white/40 to-transparent pointer-events-none" />

                    <div className="relative z-10 flex justify-between items-center mb-4 text-white">
                      <span className="font-black text-lg drop-shadow-sm">
                        {idx + 1}. Option {option.option_id}
                      </span>
                      <span className="font-mono text-2xl font-black drop-shadow-sm">
                        {option.score.toFixed(2)}
                      </span>
                    </div>

                    <div className="relative z-10 space-y-2">
                      {sortReasons(option.reasons)
                        .slice(0, 4)
                        .map((reason, rIdx) => (
                          <div
                            key={rIdx}
                            className="text-xs font-bold text-white/90 truncate flex items-start gap-2"
                          >
                            <CheckCircle2
                              size={14}
                              className={`shrink-0 ${isWinner ? "text-green-300" : "text-blue-300"}`}
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
                        <p className="text-[10px] text-white/60 font-black italic pl-5 tracking-tighter uppercase">
                          + {option.reasons.length - 4} more factors
                        </p>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="lg:col-span-2">
            <h3 className="font-black text-white uppercase tracking-widest text-xs flex items-center gap-2 mb-6 ml-4 drop-shadow-md">
              <FileText className="text-blue-200 drop-shadow-sm" size={18} />
              Strategic Directive
            </h3>

            <div className="relative bg-white/40 backdrop-blur-3xl border border-white/70 rounded-[3rem] p-10 shadow-2xl min-h-[500px] overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-[15%] bg-gradient-to-b from-white/40 to-transparent pointer-events-none" />

              <article className="relative z-10 prose prose-slate prose-sm sm:prose-base max-w-none">
                {result && result.consultant_report ? (
                  <ReactMarkdown
                    components={{
                      h1: ({ node, ...props }: MarkdownHeaderProps) => {
                        void node;
                        return (
                          <h1
                            className="text-3xl font-black mt-8 mb-4 text-slate-900 border-b-2 border-slate-900/10 pb-2"
                            {...props}
                          />
                        );
                      },
                      h2: ({ node, ...props }: MarkdownHeaderProps) => {
                        void node;
                        return (
                          <h2
                            className="text-xl font-black mt-10 mb-4 text-[#003366] drop-shadow-sm uppercase tracking-tight"
                            {...props}
                          />
                        );
                      },
                      h3: ({ node, ...props }: MarkdownHeaderProps) => {
                        void node;
                        return (
                          <h3
                            className="text-lg font-black mt-6 mb-2 text-slate-800"
                            {...props}
                          />
                        );
                      },
                      p: ({ node, ...props }: MarkdownHeaderProps) => {
                        void node;
                        return (
                          <p
                            className="mb-4 leading-relaxed text-slate-800 font-medium"
                            {...props}
                          />
                        );
                      },
                      ul: ({
                        node,
                        ...props
                      }: React.HTMLAttributes<HTMLUListElement> &
                        ExtraProps) => {
                        void node;
                        return (
                          <ul
                            className="list-disc list-outside ml-6 mb-6 space-y-2 text-slate-800 font-medium"
                            {...props}
                          />
                        );
                      },
                      li: ({
                        node,
                        ...props
                      }: React.LiHTMLAttributes<HTMLLIElement> &
                        ExtraProps) => {
                        void node;
                        return <li className="pl-1" {...props} />;
                      },
                      code({
                        node,
                        inline,
                        className,
                        children,
                        ...props
                      }: MarkdownCodeProps) {
                        void node;
                        const match = /language-(\w+)/.exec(className || "");
                        const isMermaid = match && match[1] === "mermaid";

                        if (!inline && isMermaid) {
                          const cleanChart = String(children)
                            .replace(/\u00A0/g, " ") // Replaces non-breaking spaces with normal spaces
                            .replace(/\n$/, "");

                          return (
                            <span className="block my-8 p-6 bg-white/20 backdrop-blur-xl rounded-[2.5rem] border border-white/60 shadow-inner overflow-x-auto">
                              <MermaidChart chart={cleanChart} />
                            </span>
                          );
                        }

                        return !inline ? (
                          <div className="mockup-code bg-[#1e293b] text-blue-100 rounded-2xl p-6 my-6 overflow-x-auto shadow-2xl border-t border-white/10">
                            <code className={className} {...props}>
                              {children}
                            </code>
                          </div>
                        ) : (
                          <code
                            className="bg-white/60 text-blue-900 px-2 py-0.5 rounded-md text-sm font-black border border-white shadow-sm"
                            {...props}
                          >
                            {children}
                          </code>
                        );
                      },
                    }}
                  >
                    {result.consultant_report}
                  </ReactMarkdown>
                ) : (
                  <div className="flex flex-col items-center justify-center h-[400px] text-white">
                    <Loader2 className="animate-spin mb-4" size={48} />
                    <p className="font-black italic tracking-widest uppercase drop-shadow-md">
                      Initializing Strategy...
                    </p>
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
