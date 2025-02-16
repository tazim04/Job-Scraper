import axios from "axios";
import { logInfo, logError } from "../utils/logger";

export const fetchAnalysis = async (
  resume_path: string,
  link: string
): Promise<any | null> => {
  try {
    // const cookies = await getLinkedInCookies();
    logInfo("Sending resume path to Flask API for analysis...", {
      resume_path,
      link,
      // cookies,
    });

    const response = await axios.post(
      "http://127.0.0.1:5001/api/compare",
      {
        resume_path,
        link,
        // cookies,
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
    if (axios.isAxiosError(error)) {
      logError("Axios error while fetching analysis:", {
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

// // helper method for getting linkedin auth
// const getLinkedInCookies = async (): Promise<any[]> => {
//   return new Promise((resolve, reject) => {
//     chrome.runtime.sendMessage({ action: "getCookies" }, (cookies) => {
//       if (chrome.runtime.lastError) {
//         reject(new Error(chrome.runtime.lastError.message));
//       } else {
//         resolve(cookies);
//       }
//     });
//   });
// };
