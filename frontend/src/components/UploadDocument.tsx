import { useState } from "react";
import { useUploadDocument } from "../hooks/useDecision";
import {
  UploadCloud,
  FileText,
  Loader2,
  CheckCircle,
  AlertCircle,
} from "lucide-react";

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
    <div className="w-full max-w-md mx-auto">
      <div
        className={`relative flex flex-col items-center justify-center w-full h-48 border-2 border-dashed rounded-xl transition-all duration-200 ease-in-out
          ${dragActive ? "border-indigo-500 bg-indigo-50" : "border-slate-300 bg-slate-50"}
          ${isSuccess ? "border-green-500 bg-green-50" : ""}
          ${isError ? "border-red-500 bg-red-50" : ""}
        `}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <label className="flex flex-col items-center justify-center w-full h-full cursor-pointer">
          {isPending && (
            <div className="flex flex-col items-center text-indigo-600 animate-pulse">
              <Loader2 className="w-10 h-10 mb-2 animate-spin" />
              <p className="text-sm font-semibold">Analyzing Document...</p>
            </div>
          )}

          {!isPending && isSuccess && (
            <div className="flex flex-col items-center text-green-600">
              <CheckCircle className="w-10 h-10 mb-2" />
              <p className="text-sm font-semibold">Upload Complete!</p>
              <p className="text-xs text-green-500 mt-1">Upload another?</p>
            </div>
          )}

          {!isPending && isError && (
            <div className="flex flex-col items-center text-red-500">
              <AlertCircle className="w-10 h-10 mb-2" />
              <p className="text-sm font-semibold">Upload Failed</p>
              <p className="text-xs mt-1">Try again</p>
            </div>
          )}

          {!isPending && !isSuccess && !isError && (
            <>
              <div className="p-4 bg-white rounded-full shadow-sm mb-3">
                <UploadCloud
                  className={`w-8 h-8 ${dragActive ? "text-indigo-600" : "text-slate-400"}`}
                />
              </div>
              <p className="mb-2 text-sm text-slate-700 font-medium">
                <span className="font-bold text-indigo-600">
                  Click to upload
                </span>{" "}
                or drag and drop
              </p>
              <p className="text-xs text-slate-500 flex items-center gap-1">
                <FileText size={12} /> PDF (MAX. 10MB)
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
