export type User = {
  name: string;
  email: string;
  picture: string;
} | null; // user can start as null

export default User;

// attributes based off of what we get from google OAuth2
