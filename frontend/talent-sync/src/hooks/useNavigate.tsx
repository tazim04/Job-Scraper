import {
  createContext,
  useContext,
  useState,
  ReactNode,
  useEffect,
} from "react";
import { useUser } from "../context/userContext";
import { logInfo } from "../utils/logger";
import NavigateOptions from "../types/navigation/NavigateOptions";
import { Page, SubPage } from "../types/navigation/Page";
import JobResult from "../types/JobResult";

// Define context type
type NavigateContextType = {
  currentPage: Page;
  subPage: SubPage;
  resultsData: JobResult | null;
  updateMode: boolean;
  navigate: (options: NavigateOptions) => void;
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
  const [updateMode, setUpdateMode] = useState(false);
  const [resultsData, setResultsData] = useState<JobResult | null>(null);
  const { user } = useUser();

  // Set subPage based on user's resume availability when they log in
  useEffect(() => {
    if (user) {
      setCurrentPage("dashboard");
      logInfo("useEffect in useNavigate.tsx!");
      logInfo("User: ", user);
      setSubPage(user.resumeUrl ? "scanner" : "upload");
    } else {
      setCurrentPage("login");
      setSubPage(null);
    }
  }, [user]);

  // update is to optionally render a back button for the upload page if the user is UPDATING their resume, not uploading a brand new one upon account creation
  const navigate = ({ page, subPage, data, update }: NavigateOptions) => {
    setCurrentPage(page);
    setSubPage(subPage ?? null);
    setUpdateMode(!!update);
    if (subPage === "results") {
      setResultsData(data || null);
    }
  };

  const clearResults = () => {
    setResultsData(null); // Clear results data when navigating away
  };

  return (
    <NavigateContext.Provider
      value={{
        currentPage,
        subPage,
        updateMode,
        resultsData,
        navigate,
        clearResults,
      }}
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
