import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCreateDecision } from "../hooks/useDecision";
import { ArrowRight, Loader2 } from "lucide-react";

const HomePage = () => {
  const [title, setTitle] = useState<string>("");
  const navigate = useNavigate();
  const { mutate: create, isPending } = useCreateDecision();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;
    create(title, {
      onSuccess: (newDecision) => {
        if (newDecision?.id) navigate(`/decisions/${newDecision.id}`);
      },
    });
  };

  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen px-4 overflow-hidden bg-linear-to-br from-[#0078D7] via-[#24e0ff] to-[#72ff8d]">
      <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-white/20 blur-[120px] rounded-full animate-pulse" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-emerald-300/40 blur-[150px] rounded-full" />

      <div className="relative w-full max-w-lg p-10 bg-white/40 backdrop-blur-3xl rounded-[3rem] border border-white/60 shadow-[0_25px_50px_-12px_rgba(0,0,0,0.25)] overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-[40%] bg-linear-to-b from-white/50 to-transparent pointer-events-none" />

        <div className="relative z-10">
          <h1 className="mb-2 text-5xl font-black text-center text-white/70 drop-shadow-sm">
            ARBITER ENGINE
          </h1>
          <p className="mb-10 font-bold text-center text-white/70">
            Analyze trade-offs. Make the right call.
          </p>
          {/* <div className="absolute top-0 left-0 w-full h-[45%] bg-linear-to-b from-white/40 to-transparent" /> */}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="group">
              <label className="block mb-2 ml-2 text-xs font-black tracking-widest text-white uppercase">
                What decision are you making?
              </label>
              <input
                type="text"
                placeholder="e.g. Should we migrate to AWS?"
                className="w-full p-5 text-lg font-medium transition-all bg-white border-2 shadow-inner rounded-2xl border-white/80 focus:ring-4 focus:ring-black/10 outline-none placeholder:text-slate-400 text-slate-800"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </div>

            <button
              type="submit"
              disabled={!title.trim() || isPending}
              className="relative flex items-center justify-center w-full gap-3 p-5 text-xl font-black text-white transition-all overflow-hidden rounded-2xl
                bg-white/10 hover:brightness-110 active:scale-[0.98]
                shadow-[0_8px_20px_rgba(0,120,215,0.4)]
                border-t border-white/50 disabled:opacity-50"
            >
              <div className="absolute top-0 left-0 w-full h-[45%] bg-gradient-to-b from-white/40 to-transparent" />

              <span className="relative z-10 drop-shadow-md">
                {isPending ? (
                  <Loader2 className="animate-spin" />
                ) : (
                  "Start Analysis"
                )}
              </span>
              {!isPending && (
                <ArrowRight
                  size={24}
                  className="relative z-10 transition-transform group-hover:translate-x-1"
                />
              )}
            </button>
          </form>
        </div>
      </div>

      {/* Footer Branding (Vista style) */}
      <div className="mt-8 text-sm font-bold text-white/80 drop-shadow-md">
        © 2026 Arbiter Systems Corp
      </div>
    </div>
  );
};

export default HomePage;
