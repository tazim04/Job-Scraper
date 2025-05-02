import axios from "axios";
import { logInfo, logError } from "../utils/logger";
import { LambdaClient, InvokeCommand } from "@aws-sdk/client-lambda";
import { AWSCredentials } from "../types/AWSCredentials";

const REGION = import.meta.env.VITE_AWS_REGION;

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

    // Get signed URL from Lambda
    const signedUrlRes = await axios.post(
      "https://duzydv33oa.execute-api.ca-central-1.amazonaws.com/default/talentSyncDownload",
      { email }
    );

    const signedUrl = signedUrlRes.data.uploadUrl;

    logInfo("Signed URL received, uploading to S3...", signedUrl);

    // Upload file directly to S3 bucket using the URL
    await axios.put(signedUrl, file, {
      headers: {
        "Content-Type": file.type || "application/pdf", // Properly set the content type
      },
    });

    logInfo("Resume uploaded directly to S3!");

    // Return public location
    const publicUrl = signedUrl.split("?")[0]; // Remove query params
    return publicUrl;

    // const response = await axios.post(
    //   "http://127.0.0.1:5001/api/upload_resume",
    //   formData,
    //   {
    //     headers: {
    //       "Content-Type": "multipart/form-data", // Required for file uploads
    //     },
    //   }
    // );

    // logInfo("Resume uploaded successfully!", response.data);
    // return response.data.resume_url;
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

export const getResumeUrl = async (
  email: string,
  awsCredentials: AWSCredentials
): Promise<string | null> => {
  const lambda = new LambdaClient({
    region: REGION,
    credentials: awsCredentials,
  });

  const payload = { email };

  const command = new InvokeCommand({
    FunctionName: "talentSyncDownload",
    Payload: new TextEncoder().encode(JSON.stringify(payload)), // Must encode
  });

  const response = await lambda.send(command);

  // Decode payload buffer
  const decodedPayload = new TextDecoder("utf-8").decode(response.Payload);
  const outerJson = JSON.parse(decodedPayload);

  // Parse the inner body if it exists
  const parsed = outerJson.body ? JSON.parse(outerJson.body) : {};

  return parsed.resumeUrl || null;
};
