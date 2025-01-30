import {
  createContext,
  useContext,
  useState,
  ReactNode,
  useEffect,
} from "react";
import { useUser } from "../context/userContext";

// Define possible pages & sub-pages
type Page = "login" | "dashboard";
type SubPage = "upload" | "scanner" | null; // Only if logged in

// Define context type
type NavigateContextType = {
  currentPage: Page;
  subPage: SubPage;
  navigate: (page: Page, subPage?: SubPage) => void;
};

// Create a context with a default undefined value
const NavigateContext = createContext<NavigateContextType | undefined>(
  undefined
);

// Create the provider component
export const NavigateProvider = ({ children }: { children: ReactNode }) => {
  const [currentPage, setCurrentPage] = useState<Page>("login");
  const [subPage, setSubPage] = useState<SubPage>(null);
  const { user } = useUser();

  // Set subPage based on user's resume availability when they log in
  useEffect(() => {
    if (user) {
      setCurrentPage("dashboard");
      setSubPage(user.resumeUrl ? "scanner" : "upload");
    } else {
      setCurrentPage("login");
      setSubPage(null);
    }
  }, [user]);

  const navigate = (page: Page, sub?: SubPage) => {
    setCurrentPage(page);
    setSubPage(sub ?? null);
  };

  return (
    <NavigateContext.Provider value={{ currentPage, subPage, navigate }}>
      {children}
    </NavigateContext.Provider>
  );
};

// Custom hook to use navigation context
export const useNavigate = (): NavigateContextType => {
  const context = useContext(NavigateContext);
  if (!context) {
    throw new Error("useNavigate must be used within a NavigateProvider");
  }
  return context;
};
