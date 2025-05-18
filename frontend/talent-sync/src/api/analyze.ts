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

    // Validate LinkedIn job link
    const isLinkedInJobUrl =
      typeof link === "string" &&
      link.includes("linkedin.com/jobs") &&
      (link.includes("currentJobId=") || /\/jobs\/view\/\d+/.test(link));

    if (!isLinkedInJobUrl) {
      logError("Invalid LinkedIn job link detected.", link);
      return {
        error: "Invalid Job Link",
        reason: "Please provide a valid LinkedIn job posting.",
      };
    }

    const lambda = new LambdaClient({
      region: REGION,
      credentials: awsCredentials,
    });

    const payload = { resume_path, link };

    const command = new InvokeCommand({
      FunctionName: "talentSyncAnalyzer",
      Payload: JSON.stringify(payload),
    });

    const response = await lambda.send(command);

    // Decode payload buffer
    const decodePayload = new TextDecoder("utf-8").decode(response.Payload);
    logInfo("RAW Lambda Payload:", decodePayload);

    const outerJson = JSON.parse(decodePayload);

    // Status code handling from Python lambda response
    const statusCode = outerJson.statusCode;
    const parsedAnalysis = outerJson.body ? JSON.parse(outerJson.body) : {};

    if (statusCode !== 200) {
      const rawError = parsedAnalysis.error;

      let friendlyMessage =
        rawError || "An unknown error occurred during analysis.";

      // Detect Groq rate limit error
      const isRateLimitError =
        typeof rawError === "string" &&
        rawError.includes("rate_limit_exceeded") &&
        rawError.includes("tokens per day");

      if (isRateLimitError) {
        friendlyMessage = `We've reached our current AI usage limit. Please try again tomorrow.`;
      }

      return {
        error: "Analysis Failed",
        reason: friendlyMessage,
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
