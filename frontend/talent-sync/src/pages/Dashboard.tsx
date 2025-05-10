import Greeting from "../components/Greeting";

const Dashboard: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="p-5">
      <Greeting />

      {/* Either Job Scanner, Resume Upload or Results */}
      <div className="mt-2">{children}</div>
    </div>
  );
};

export default Dashboard;
