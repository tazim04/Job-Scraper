import "./App.css";
import { Loader2 } from "lucide-react";
import { useUser } from "./context/userContext";
import { NavigateProvider, useNavigate } from "./hooks/useNavigate";

// Components
import Header from "./components/Header";
import Login from "./pages/Login";
import UploadResume from "./pages/UploadResume";
import JobScanner from "./pages/JobScanner";
import Dashboard from "./pages/Dashboard";
import Results from "./pages/Results";

const App: React.FC = () => {
  return (
    <NavigateProvider>
      <MainApp />
    </NavigateProvider>
  );
};

const MainApp: React.FC = () => {
  const { user, loading } = useUser();
  const { currentPage, subPage } = useNavigate();

  return (
    <div className="w-[24rem] h-[26rem] font-sans">
      <Header />

      {loading ? (
        <div className="flex flex-col items-center justify-center h-[50vh]">
          <Loader2 className="animate-spin text-indigo-500" size={32} />
          <h3 className="mt-2 text-gray-700 text-lg font-medium">Loading...</h3>
        </div>
      ) : currentPage === "login" && !user ? (
        <Login />
      ) : (
        user && (
          <Dashboard>
            {subPage === "upload" && <UploadResume />}
            {subPage === "scanner" && <JobScanner />}
            {subPage === "results" && <Results />}
          </Dashboard>
        )
      )}
    </div>
  );
};

export default App;
