import { createContext, useContext, useEffect, useState } from "react";
import User from "../types/user";
import { getChromeStorage, setChromeStorage } from "../utils/chromeStorage";
import { getResumeUrl } from "../api/resume";
import { AWSCredentials } from "../types/AWSCredentials";
import { useAuth } from "../hooks/useAuth";

// Define Context Type
type UserContextType = {
  user: User;
  setUser: (user: User) => void; // Take User, return void
  loading: boolean;
};

// Check if AWS credentials are still valid
const isAWSCredentialsValid = (credentials: AWSCredentials): boolean => {
  if (!credentials || typeof credentials.expiresAt !== "number") return false; // If no credentials, or credentials is not a number, false
  const now = Date.now();
  return now < credentials.expiresAt; // Check if the credentials have expired
};

// Create Context
const UserContext = createContext<UserContextType | undefined>(undefined);

// Custom Hook
export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) throw new Error("useUser must be used within a UserProvider");
  return context;
};

// User Provider
export const UserProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User>(null);
  const [loading, setLoading] = useState(true);
  const { getAWSCredsFromIdToken } = useAuth();

  // Load user from Chrome Storage on mount
  useEffect(() => {
    const initUser = async () => {
      try {
        const storedUser = await getChromeStorage("user");

        // Check if AWS credentials are still valid
        const validCreds = isAWSCredentialsValid(storedUser?.awsCredentials);

        // Expired, get new credentials
        if (!validCreds) {
          if (storedUser?.idToken) {
            const newCreds = await getAWSCredsFromIdToken(storedUser.idToken); // Get new creds if existing idToken
            storedUser.awsCredentials = newCreds;
            await setChromeStorage("user", storedUser);
          } else {
            // fallback: re-prompt login
            setUser(null);
            return;
          }
        }

        // Update resume URL
        const resumeUrl = await getResumeUrl(
          storedUser.email,
          storedUser.awsCredentials
        );
        setUser({ ...storedUser, resumeUrl });
      } catch (err) {
        console.warn("Error initializing user:", err);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    initUser();

    // Listen for storage updates
    const handleStorageChange = (changes: {
      [key: string]: chrome.storage.StorageChange;
    }) => {
      if ("user" in changes) {
        setUser(changes.user.newValue || null);
      }
    };

    chrome.storage.onChanged.addListener(handleStorageChange);
    return () => chrome.storage.onChanged.removeListener(handleStorageChange);
  }, []);

  // Save user to Chrome Storage whenever it changes
  const updateUser = (newUser: User) => {
    setUser(newUser);
    setChromeStorage("user", newUser).catch((err) =>
      console.error("Error saving user to storage:", err)
    );
  };

  return (
    <UserContext.Provider value={{ user, setUser: updateUser, loading }}>
      {children}
    </UserContext.Provider>
  );
};
