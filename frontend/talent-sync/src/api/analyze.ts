import { logInfo, logError } from "../utils/logger";
import { LambdaClient, InvokeCommand } from "@aws-sdk/client-lambda";
import { AWSCredentials } from "../types/AWSCredentials";

const REGION = import.meta.env.VITE_AWS_REGION;

export const fetchAnalysis = async (
  resume_path: string,
  link: string,
  awsCredentials: AWSCredentials
): Promise<any | null> => {
  try {
    logInfo("Calling Lambda API for analysis...", {
      resume_path,
      link,
    });

    const lambda = new LambdaClient({
      region: REGION,
      credentials: awsCredentials,
    });

    const payload = { resume_path, link };

    const command = new InvokeCommand({
      FunctionName: "talentSyncAnalyzer",
      Payload: new TextEncoder().encode(JSON.stringify(payload)),
    });

    const response = await lambda.send(command);

    // Decode payload buffer
    const decodePayload = new TextDecoder("utf-8").decode(response.Payload);
    const outerJson = JSON.parse(decodePayload);

    // Status code handling from Python lambda response
    const statusCode = outerJson.statusCode;
    const parsedAnalysis = outerJson.body ? JSON.parse(outerJson.body) : {};

    if (statusCode !== 200) {
      return {
        error: "Analysis Failed",
        reason:
          parsedAnalysis.error || "An unknown error occurred during analysis.",
      };
    }

    logInfo("Analysis received successfully!", parsedAnalysis);
    return parsedAnalysis;
  } catch (error) {
    logError("Unexpected error calling Lambda:", error);
    return {
      error: "Unexpected Error",
      reason: "Something went wrong. Please try again later.",
    };
  }
};

// export const fetchAnalysis = async (
//   resume_path: string,
//   link: string
// ): Promise<any | null> => {
//   try {
//     logInfo("Sending resume path to backend API for analysis...", {
//       resume_path,
//       link,
//     });

//     const response = await axios.post(
//       "http://127.0.0.1:5001/api/compare",
//       {
//         resume_path,
//         link,
//       },
//       {
//         headers: {
//           "Content-Type": "application/json",
//         },
//       }
//     );

//     logInfo("Analysis received successfully!", response.data);
//     return response.data;
//   } catch (error) {
//     if (axios.isAxiosError(error)) {
//       logInfo("Axios error caught.");

//       const errorMessage = error.response?.data?.error ?? "";

//       const limitExceeded =
//         typeof errorMessage === "string" &&
//         errorMessage.includes("Error code: 429");

//       if (limitExceeded) {
//         const retryMatch = errorMessage.match(
//           /Please try again in (\d+)m(\d+\.\d+)s/
//         );
//         const retryMinutes = retryMatch ? parseInt(retryMatch[1], 10) : 0;
//         const retrySeconds = retryMatch ? parseFloat(retryMatch[2]) : 0;

//         return {
//           error: "Rate Limit Exceeded",
//           reason: `TalentSync has temporarily reached its processing limit. Please try again in ${retryMinutes}m ${Math.round(
//             retrySeconds
//           )}s.`,
//         };
//       }

//       return {
//         error: "Analysis Failed",
//         reason: errorMessage || "An unknown error occurred.",
//       };
//     }

//     logError("Unexpected non-Axios error:", error);
//     return {
//       error: "Unexpected Error",
//       reason: "Something went wrong. Please try again later.",
//     };
//   }
// };
