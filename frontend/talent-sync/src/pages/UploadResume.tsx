import { useState } from "react";
import { useNavigate } from "../hooks/useNavigate";

const UploadResume = () => {
  const [file, setFile] = useState<File | null>(null);
  const { navigate } = useNavigate();

  const handleUpload = () => {
    if (file) {
      // TODO: Upload file to cloud storage
      console.log("Uploading resume:", file.name);
      navigate("dashboard", "scanner");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-2xl mb-4">Upload Your Resume</h1>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button
        onClick={handleUpload}
        className="bg-green-500 text-white px-4 py-2 rounded mt-4"
        disabled={!file}
      >
        Upload & Continue
      </button>
    </div>
  );
};

export default UploadResume;
