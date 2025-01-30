import { useState } from "react";
import { useNavigate } from "../hooks/useNavigate";
import FileUploader from "../components/FileUploader";

const UploadResume = () => {
  const [file, setFile] = useState<File | null>(null);
  const { navigate } = useNavigate();

  const handleUpload = () => {
    if (!file) return;

    // TODO: Upload file to cloud storage
    console.log("Uploading resume:", file.name);

    // Navigate to scanner after upload
    navigate("dashboard", "scanner");
  };

  return (
    <div className="flex flex-col items-center justify-center h-[50vh] text-center">
      <h1 className="text-base mb-2">Upload Your Resume</h1>
      <FileUploader setFile={setFile} />

      {file && (
        <p className="mt-3 text-sm text-gray-600">
          Selected file: <strong>{file.name}</strong>
        </p>
      )}

      <button
        onClick={handleUpload}
        className="bg-emerald-500 text-white px-4 py-2 rounded mt-4 disabled:opacity-50"
        disabled={!file}
      >
        Upload & Continue
      </button>
    </div>
  );
};

export default UploadResume;
