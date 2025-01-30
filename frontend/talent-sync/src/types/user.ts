export type User = {
  name: string;
  email: string;
  picture: string;
  resumeUrl?: string; // URL to uploaded resume (S3)
} | null; // user can start as null

export default User;

// attributes based off of what we get from google OAuth2
