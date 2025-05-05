import { AWSCredentials } from "./AWSCredentials";

export type User = {
  name: string;
  email: string;
  picture: string;
  resumeUrl?: string; // URL to uploaded resume (S3)
  awsCredentials: AWSCredentials; // required to make trigger Lambda functions
  idToken?: string;
  accessToken?: string;
} | null; // user can start as null

export default User;

// attributes based off of what we get from google OAuth2
