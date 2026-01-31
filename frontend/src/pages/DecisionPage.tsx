import { useParams } from "react-router-dom";
import UploadDocument from "../components/UploadDocument";
import DecisionResult from "../components/DecisionResult";

const DecisionPage = () => {
  const { id } = useParams();
  const decisionId = Number(id);

  if (isNaN(decisionId)) return <div>Invalid ID</div>;
  return (
    <div className="max-w-7xl mx-auto p-6 lg:p-10">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900">
          Decision #{decisionId}
        </h1>
        <p className="text-slate-500">Project Workspace</p>
      </header>

      <div className="grid grid-cols-1 gap-10">
        <section className="bg-slate-50 p-6 rounded-2xl border border-slate-200">
          <h2 className="text-lg font-semibold text-slate-800 mb-4 flex items-center gap-2">
            1. Add Evidence
            <span className="text-xs font-normal text-slate-500 bg-white px-2 py-1 rounded-full border">
              PDF Support
            </span>
          </h2>
          <UploadDocument decisionId={decisionId} />
        </section>

        <section>
          <DecisionResult decisionId={decisionId} />
        </section>
      </div>
    </div>
  );
};

export default DecisionPage;
