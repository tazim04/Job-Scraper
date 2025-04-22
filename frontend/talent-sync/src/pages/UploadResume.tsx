import { useState } from "react";
import { useNavigate } from "../hooks/useNavigate";
import { uploadResume } from "../api/resume";
import FileUploader from "../components/FileUploader";
import { useUser } from "../context/userContext";
import { logInfo, logError, logWarn } from "../utils/logger";

const UploadResume = () => {
  const [file, setFile] = useState<File | null>(null);
  const { user, setUser } = useUser();
  const { navigate } = useNavigate();
  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    if (!file || !user) {
      logWarn("Upload aborted: No file or user found.");
      return;
    }

    setUploading(true); // Start uploading
    logInfo("Uploading resume...", { fileName: file.name, email: user.email });

    try {
      // Call the API to upload the resume
      const resumeUrl = await uploadResume(file, user.email);

      logInfo("resumeUrl", { resumeUrl });

      if (resumeUrl) {
        logInfo("Upload successful!", { resumeUrl });

        // Update user context with the resume URL
        setUser({ ...user, resumeUrl });

        // Navigate to the scanner page
        navigate("dashboard", "scanner");
      } else {
        logError("Upload failed: No resume URL received.");
      }
    } catch (error) {
      logError("Upload error:", error);
    } finally {
      setUploading(false); // Reset uploading state
    }
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
        className="bg-green-500 text-white px-4 py-2 rounded mt-4 disabled:opacity-50"
        disabled={!file || uploading}
      >
        {uploading ? "Uploading..." : "Upload & Continue"}
      </button>
    </div>
  );
};

export default UploadResume;
