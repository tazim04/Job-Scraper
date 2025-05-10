import { useState } from "react";
import { useNavigate } from "../hooks/useNavigate";
import { getResumeUrl, uploadResume } from "../api/resume";
import FileUploader from "../components/FileUploader";
import { useUser } from "../context/userContext";
import { logInfo, logError, logWarn } from "../utils/logger";
import NavigateOptions from "../types/navigation/NavigateOptions";

const UploadResume = () => {
  const [file, setFile] = useState<File | null>(null);
  const { user, setUser } = useUser();
  const { navigate, updateMode } = useNavigate();
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
      const success = await uploadResume(file, user.email, user.awsCredentials);

      if (success) {
        logInfo("Upload successful!");

        // get fresh signed resume url
        const signedResumeUrl = await getResumeUrl(
          user.email,
          user.awsCredentials
        );

        // Update user context with the resume URL
        setUser({ ...user, resumeUrl: signedResumeUrl });

        // Navigate to the scanner page
        const payload: NavigateOptions = {
          page: "dashboard",
          subPage: "scanner",
        };
        navigate(payload);
      } else {
        logError("Upload failed: No resume URL received.");
      }
    } catch (error) {
      logError("Upload error:", error);
    } finally {
      setUploading(false); // Reset uploading state
    }
  };

  const handleBack = () => {
    const payload: NavigateOptions = {
      page: "dashboard",
      subPage: "scanner",
    };
    navigate(payload);
  };

  return (
    <div className="flex flex-col items-center justify-center h-[54vh] text-center mb-5">
      {updateMode && (
        <button
          onClick={handleBack}
          className="bg-indigo-500 text-white px-4 py-2 rounded my-4 transition-colors ease-in-out hover:bg-indigo-400"
        >
          Back to Scanner
        </button>
      )}
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
