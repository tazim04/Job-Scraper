import axios from "axios";
import { logInfo, logError } from "../utils/logger";

export const fetchAnalysis = async (
  resume_path: string,
  link: string
): Promise<any | null> => {
  try {
    logInfo("Sending resume path to backend API for analysis...", {
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
          "Content-Type": "application/json",
        },
      }
    );

    logInfo("Analysis received successfully!", response.data);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      logInfo("Axios error caught.");

      const errorMessage = error.response?.data?.error ?? "";

      const limitExceeded =
        typeof errorMessage === "string" &&
        errorMessage.includes("Error code: 429");

      if (limitExceeded) {
        const retryMatch = errorMessage.match(
          /Please try again in (\d+)m(\d+\.\d+)s/
        );
        const retryMinutes = retryMatch ? parseInt(retryMatch[1], 10) : 0;
        const retrySeconds = retryMatch ? parseFloat(retryMatch[2]) : 0;

        return {
          error: "Rate Limit Exceeded",
          reason: `TalentSync has temporarily reached its processing limit. Please try again in ${retryMinutes}m ${Math.round(
            retrySeconds
          )}s.`,
        };
      }

      return {
        error: "Analysis Failed",
        reason: errorMessage || "An unknown error occurred.",
      };
    }

    logError("Unexpected non-Axios error:", error);
    return {
      error: "Unexpected Error",
      reason: "Something went wrong. Please try again later.",
    };
  }
};
