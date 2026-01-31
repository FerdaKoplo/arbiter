import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCreateDecision } from "../hooks/useDecision";
import { ArrowRight, BrainCircuit, Loader2 } from "lucide-react";

const HomePage = () => {
  const [title, setTitle] = useState<string>("");
  const navigate = useNavigate();

  const { mutate: create, isPending } = useCreateDecision();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    create(title, {
      onSuccess: (newDecision) => {
        console.log("SERVER RESPONSE:", newDecision); // <--- Add this!

        if (newDecision && newDecision.id) {
          navigate(`/decisions/${newDecision.id}`);
        } else {
          alert("Error: No ID returned. Check Console.");
        }
      },
      onError: (error) => {
        console.error("API ERROR:", error);
        alert("Failed to create decision.");
      },
    });
  };
  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4 bg-slate-50">
      <div className="w-full max-w-lg p-8 bg-white border shadow-xl rounded-2xl border-slate-100">
        <div className="flex justify-center mb-6 text-indigo-600">
          <BrainCircuit size={64} strokeWidth={1.5} />
        </div>

        <h1 className="mb-2 text-3xl font-bold text-center text-slate-800">
          Arbiter Engine
        </h1>
        <p className="mb-8 text-center text-slate-500">
          Upload evidence. Analyze trade-offs. Make the right call.
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block mb-2 text-sm font-semibold text-slate-700">
              What decision are you making?
            </label>
            <input
              type="text"
              placeholder="e.g. Should we migrate to AWS or stay on-prem?"
              className="w-full p-4 text-lg border-2 rounded-xl border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              autoFocus
            />
          </div>

          <button
            type="submit"
            disabled={!title.trim() || isPending}
            className="flex items-center justify-center w-full gap-2 p-4 text-lg font-bold text-white transition-all bg-indigo-600 rounded-xl hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isPending ? (
              <>
                <Loader2 className="animate-spin" /> Creating Project...
              </>
            ) : (
              <>
                Start Analysis <ArrowRight size={20} />
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default HomePage;
