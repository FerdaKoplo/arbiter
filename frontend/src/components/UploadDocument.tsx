import { useState } from "react";
import { useUploadDocument } from "../hooks/useDecision";
import { UploadCloud, FileText, Loader2, CheckCircle } from "lucide-react";

interface UploadDocumentProps {
  decisionId: number;
}

const UploadDocument: React.FC<UploadDocumentProps> = ({ decisionId }) => {
  const [dragActive, setDragActive] = useState<boolean>(false);
  const { mutate: upload, isPending, isSuccess, isError } = useUploadDocument();

  const handleFile = (file: File) => {
    if (file && file.type === "application/pdf") {
      upload({ decisionId, file });
    } else {
      alert("Please upload a PDF file.");
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="w-full max-w-xl mx-auto">
      <div
        className={`relative flex flex-col items-center justify-center w-full h-56 border-2 border-dashed rounded-3xl transition-all duration-300
          ${dragActive ? "border-white bg-white/40 scale-[1.02]" : "border-white/40 bg-white/10"}
          ${isSuccess ? "border-green-400 bg-green-400/20" : ""}
          ${isError ? "border-red-400 bg-red-400/20" : ""}
        `}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <label className="flex flex-col items-center justify-center w-full h-full cursor-pointer">
          {isPending ? (
            <div className="flex flex-col items-center text-white">
              <Loader2 className="w-12 h-12 mb-3 animate-spin drop-shadow-md" />
              <p className="text-lg font-black tracking-tight">
                ANALYZING DOCUMENT...
              </p>
            </div>
          ) : isSuccess ? (
            <div className="flex flex-col items-center text-white">
              <CheckCircle className="w-12 h-12 mb-3 drop-shadow-md" />
              <p className="text-lg font-black">COMPLETE</p>
            </div>
          ) : (
            <>
              <div className="p-5 bg-white/30 rounded-full shadow-lg border border-white/50 mb-4 transition-transform hover:scale-110">
                <UploadCloud className="w-10 h-10 text-white" />
              </div>
              <p className="mb-2 text-lg text-white font-black tracking-tight drop-shadow-sm text-center">
                DRAG & DROP EVIDENCE
              </p>
              <p className="text-[10px] text-white/70 font-black tracking-[0.2em] flex items-center gap-2">
                <FileText size={14} /> PDF ONLY (10MB MAX)
              </p>
            </>
          )}
          <input
            type="file"
            className="hidden"
            accept=".pdf"
            onChange={handleChange}
            disabled={isPending}
          />
        </label>
      </div>
    </div>
  );
};

export default UploadDocument;
