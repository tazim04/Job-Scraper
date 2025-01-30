import { createContext, useContext, useEffect, useState } from "react";
import User from "../types/user";
import { getChromeStorage, setChromeStorage } from "../utils/chromeStorage";
import { getResumeUrl } from "../api/resume";

// Define Context Type
type UserContextType = {
  user: User;
  setUser: (user: User) => void; // Take User, return void
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

  // Load user from Chrome Storage on mount
  useEffect(() => {
    getChromeStorage("user")
      .then(async (storedUser) => {
        if (storedUser) {
          // Fetch the resume URL from the backend
          const resumeUrl = await getResumeUrl(storedUser.email);

          // Update the user object with resumeUrl if it exists
          setUser({ ...storedUser, resumeUrl });
        } else {
          setUser(null); // Ensure user state is set to null if no data exists
        }
      })
      .catch((err) => console.warn("Error fetching user from storage:", err));

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
    <UserContext.Provider value={{ user, setUser: updateUser }}>
      {children}
    </UserContext.Provider>
  );
};
