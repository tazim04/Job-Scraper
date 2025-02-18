import axios from "axios";
import { logInfo, logError } from "../utils/logger";

export const fetchAnalysis = async (
  resume_path: string,
  link: string
): Promise<any | null> => {
  try {
    logInfo("Sending resume path to Flask API for analysis...", {
      resume_path,
      link,
    });

    const response = await axios.post(
      "http://127.0.0.1:5001/api/compare",
      {
        resume_path,
        link,
      },
      {
        headers: {
          "Content-Type": "application/json", // Sending JSON data
        },
      }
    );

    logInfo("Analysis received successfully!", response.data);
    return response.data; // Return structured analysis result
  } catch (error) {
    // Check if the error is an Axios error
    if (axios.isAxiosError(error)) {
      logInfo("axios error!");
      const errorMessage = error.response?.data?.error;

      logInfo(
        "429 error: ",
        (error.response?.data?.error).includes("Error code: 429")
      );

      const limitExceeded = errorMessage.includes("Error code: 429");

      // Handle rate limit errors
      if (limitExceeded) {
        // Extract retry time (if available)
        const retryMatch =
          typeof errorMessage === "string"
            ? errorMessage.match(/Please try again in (\d+)m(\d+\.\d+)s/)
            : null;
        const retryMinutes = retryMatch ? parseInt(retryMatch[1], 10) : 0;
        const retrySeconds = retryMatch ? parseFloat(retryMatch[2]) : 0;

        return {
          error: "Rate Limit Exceeded",
          reason: `TalentSync has temporarily reached its processing limit. Please try again in ${retryMinutes}m ${Math.round(
            retrySeconds
          )}s.`,
        };
      }

      // Handle other errors
      return {
        error: "Analysis Failed",
        reason: errorMessage || "An unknown error occurred.",
      };
    }

    // Handle non-Axios errors
    logError("Unexpected error:", error);
    return {
      error: "Unexpected Error",
      reason: "Something went wrong. Please try again later.",
    };
  }
};
