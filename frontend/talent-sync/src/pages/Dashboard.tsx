import { useNavigate } from "../hooks/useNavigate";
import Greeting from "../components/Greeting";

const Dashboard: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { navigate } = useNavigate();

  return (
    <div className="p-5">
      <Greeting />

      {/* Either Job Scanner or Resume Upload */}
      <div className="mt-5">{children}</div>
    </div>
  );
};

export default Dashboard;
