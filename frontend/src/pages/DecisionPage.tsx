import { useParams } from "react-router-dom";
import UploadDocument from "../components/UploadDocument";
import DecisionResult from "../components/DecisionResult";

const DecisionPage = () => {
  const { id } = useParams();
  const decisionId = Number(id);

  if (isNaN(decisionId)) return <div>Invalid ID</div>;
  return (
    <div className="relative min-h-screen px-4 py-10 overflow-x-hidden bg-linear-to-br from-[#0078D7] via-[#24e0ff] to-[#72ff8d]">
      <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-white/10 blur-[120px] rounded-full" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-emerald-400/20 blur-[150px] rounded-full" />

      <div className="relative z-10 max-w-7xl mx-auto">
        <header className="mb-10 ml-4">
          <h1 className="text-4xl font-black text-white/70 drop-shadow-md tracking-tight uppercase">
            Decision #{decisionId}
          </h1>
          <p className="text-white/40 drop-shadow-md font-bold tracking-widest uppercase text-xs">
            Project Workspace
          </p>
        </header>

        <div className="grid grid-cols-1 gap-10">
          <section className="relative p-8 bg-white/30 backdrop-blur-3xl rounded-[2.5rem] border border-white/50 shadow-2xl overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-[30%] bg-linear-to-b from-white/40 to-transparent pointer-events-none" />

            <h2 className="text-xl font-black text-white mb-6 flex items-center gap-3 drop-shadow-sm">
              <span className="bg-white/40 w-8 h-8 rounded-full flex items-center justify-center text-sm">
                1
              </span>
              ADD EVIDENCE
              <span className="text-[10px] font-black text-blue-900 bg-white/60 px-3 py-1 rounded-full border border-white/50">
                PDF SUPPORT
              </span>
            </h2>
            <UploadDocument decisionId={decisionId} />
          </section>

          {/* RESULTS SECTION */}
          <section className="relative">
            <DecisionResult decisionId={decisionId} />
          </section>
        </div>
      </div>
    </div>
  );
};

export default DecisionPage;
