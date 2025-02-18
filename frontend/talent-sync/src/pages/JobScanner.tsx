import { useState } from "react";
import { Loader2, FileScan, FileUser } from "lucide-react";
import { useUser } from "../context/userContext";
import { fetchAnalysis } from "../api/analyze";
import { viewResume } from "../api/resume";
import { useNavigate } from "../hooks/useNavigate";

const JobScanner = () => {
  const [scanning, setScanning] = useState(false);
  const { user } = useUser();
  const { navigate } = useNavigate();

  const handleScanJob = async () => {
    console.log("Fetching job details...");
    setScanning(true);

    chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
      const currentUrl = tabs[0]?.url || "";

      if (!user?.resumeUrl || !currentUrl) {
        console.error("Missing resume URL or current job page URL.");
        setScanning(false);
        return;
      }

      try {
        const analysisResult = await fetchAnalysis(user.resumeUrl, currentUrl);
        navigate("dashboard", "results", analysisResult);
      } catch (error) {
        console.error("Error fetching analysis:", error);
      }

      setScanning(false);
    });
  };

  const handleViewResume = () => {
    if (!user?.resumeUrl) {
      console.error("No resume URL found!");
      return;
    }
    viewResume(user.email);
  };

  return (
    <div className="flex flex-col items-center justify-center h-[43vh] p-6 gap-3">
      <button
        onClick={handleViewResume}
        className="bg-emerald-500 text-white justify-center w-52 px-5 py-3 flex items-center gap-2 rounded-lg text-lg font-medium transition-all hover:bg-emerald-400 active:-translate-y-0.5"
        disabled={scanning}
      >
        <>
          <FileUser size={20} />
          Resume
        </>
      </button>

      <button
        onClick={handleScanJob}
        className={`bg-indigo-500 text-white justify-center px-5 py-3 w-52 flex items-center gap-2 rounded-lg text-lg font-medium transition-all ease-in-out 
          ${
            scanning
              ? "opacity-50 cursor-not-allowed"
              : "hover:bg-indigo-400 active:-translate-y-0.5"
          }`}
        disabled={scanning}
      >
        {scanning ? (
          <>
            <Loader2 className="animate-spin" size={20} />
            Scanning...
          </>
        ) : (
          <>
            <FileScan size={20} />
            Scan Job
          </>
        )}
      </button>
    </div>
  );
};

export default JobScanner;
