import axios from "axios";
import { logInfo, logError } from "../utils/logger";
import { LambdaClient, InvokeCommand } from "@aws-sdk/client-lambda";
import { AWSCredentials } from "../types/AWSCredentials";

const REGION = import.meta.env.VITE_AWS_REGION;

// Update existing resume, just reuses existing logic
export const updateResume = async (
  file: File,
  email: string,
  awsCredentials: AWSCredentials
): Promise<boolean> => {
  logInfo("Updating resume for ", email);
  return uploadResume(file, email, awsCredentials);
};

// Upload resume file
export const uploadResume = async (
  file: File,
  email: string,
  awsCredentials: AWSCredentials
): Promise<boolean> => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("email", email);

  try {
    logInfo("Sending resume to Lambda API...", { fileName: file.name, email });

    const lambda = new LambdaClient({
      region: REGION,
      credentials: awsCredentials,
    });

    const payload = { email };

    const command = new InvokeCommand({
      FunctionName: "talentSyncUpload",
      Payload: JSON.stringify(payload),
    });

    const response = await lambda.send(command);

    // Decode payload buffer
    const decodePayload = new TextDecoder("utf-8").decode(response.Payload);
    const outerJson = JSON.parse(decodePayload);

    // Parse the inner body if it exists
    const parsed = outerJson.body ? JSON.parse(outerJson.body) : {};

    const uploadUrl = parsed.uploadUrl;

    if (!uploadUrl) {
      logError("[uploadResume] No signed upload URL received from Lambda.");
      return false;
    }

    logInfo("Signed URL received, uploading to S3...", uploadUrl);

    // Upload file directly to S3 bucket using the URL
    await axios.put(uploadUrl, file, {
      headers: {
        "Content-Type": file.type || "application/pdf",
      },
    });

    logInfo("Resume uploaded directly to S3!");

    return true;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      logError("[uploadResume] Axios error during S3 upload:", {
        message: error.message,
        status: error.response?.status,
        response: error.response?.data,
      });
    } else {
      logError("[uploadResume] Lambda or general error:", error);
    }
    return false;
  }
};

export const getResumeUrl = async (
  email: string,
  awsCredentials: AWSCredentials
): Promise<string | null> => {
  try {
    const lambda = new LambdaClient({
      region: REGION,
      credentials: awsCredentials,
    });

    const payload = { email };

    const command = new InvokeCommand({
      FunctionName: "talentSyncDownload",
      Payload: JSON.stringify(payload),
    });

    const response = await lambda.send(command);

    // Decode payload buffer
    const decodedPayload = new TextDecoder("utf-8").decode(response.Payload);
    const outerJson = JSON.parse(decodedPayload);

    // Parse the inner body if it exists
    const parsed = outerJson.body ? JSON.parse(outerJson.body) : {};

    return parsed.resumeUrl || null;
  } catch (error) {
    logError("[getResumeUrl] Error:", error);
    return null;
  }
};
