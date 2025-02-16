import {
  createContext,
  useContext,
  useState,
  ReactNode,
  useEffect,
} from "react";
import { useUser } from "../context/userContext";
import JobResult from "../types/JobResult";

// Define possible pages & sub-pages
type Page = "login" | "dashboard";
type SubPage = "upload" | "scanner" | "results" | null; // Only if logged in

// Define context type
type NavigateContextType = {
  currentPage: Page;
  subPage: SubPage;
  resultsData: JobResult | null;
  navigate: (page: Page, subPage?: SubPage, data?: JobResult) => void;
  clearResults: () => void;
};

// Create a context with a default undefined value
const NavigateContext = createContext<NavigateContextType | undefined>(
  undefined
);

// Create the provider component
export const NavigateProvider = ({ children }: { children: ReactNode }) => {
  const [currentPage, setCurrentPage] = useState<Page>("login");
  const [subPage, setSubPage] = useState<SubPage>(null);
  const [resultsData, setResultsData] = useState<JobResult | null>(null); // Add state for results data
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

  const navigate = (page: Page, sub?: SubPage, data?: JobResult) => {
    setCurrentPage(page);
    setSubPage(sub ?? null);
    if (sub === "results") {
      setResultsData(data || null); // Store results data when navigating to results page
    }
  };

  const clearResults = () => {
    setResultsData(null); // Clear results data when navigating away
  };

  return (
    <NavigateContext.Provider
      value={{ currentPage, subPage, resultsData, navigate, clearResults }}
    >
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
