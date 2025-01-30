import "./App.css";
import { useUser } from "./context/userContext";
import { NavigateProvider, useNavigate } from "./hooks/useNavigate";

// Components
import Header from "./components/Header";
import Login from "./pages/Login";
import UploadResume from "./pages/UploadResume";
import JobScanner from "./pages/JobScanner";
import Dashboard from "./pages/Dashboard";

const App: React.FC = () => {
  return (
    <NavigateProvider>
      <MainApp />
    </NavigateProvider>
  );
};

const MainApp: React.FC = () => {
  const { user } = useUser();
  const { currentPage, subPage } = useNavigate();

  return (
    <div className="w-96 h-[30rem] font-sans">
      <Header />
      {currentPage === "login" && !user && <Login />}
      {user && (
        <Dashboard>
          {subPage === "upload" && <UploadResume />}
          {subPage === "scanner" && <JobScanner />}
        </Dashboard>
      )}
    </div>
  );
};

export default App;
