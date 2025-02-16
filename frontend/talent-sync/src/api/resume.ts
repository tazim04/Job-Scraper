import axios from "axios";
import { logInfo, logError } from "../utils/logger";

// Upload resume file
export const uploadResume = async (
  file: File,
  email: string
): Promise<string | null> => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("email", email);

  try {
    logInfo("Sending resume to Flask API...", { fileName: file.name, email });

    const response = await axios.post(
      "http://127.0.0.1:5001/api/upload_resume",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data", // Required for file uploads
        },
      }
    );

    logInfo("Resume uploaded successfully!", response.data);
    return response.data.resumeUrl;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      logError("Axios error:", {
        message: error.message,
        response: error.response?.data || "No response data",
        status: error.response?.status || "No status",
      });
    } else {
      logError("Unexpected error:", error);
    }
    return null;
  }
};

// Get resume url if it exists
export const getResumeUrl = async (email: string): Promise<string | null> => {
  try {
    const response = await axios.post(
      "http://127.0.0.1:5001/api/get_resume_url",
      { email }
    );

    return response.data.resumeUrl; // Returns either the resume URL or null
  } catch (error) {
    console.error("Error getting resume URL:", error);
    return null;
  }
};
