import { useUser } from "../context/userContext";
import { useNavigate } from "../hooks/useNavigate";

const Header = () => {
  const { user, setUser } = useUser();
  const { navigate } = useNavigate();

  const signOut = () => {
    setUser(null);
    navigate("login");
  };
  return (
    <div className="px-5 py-3 flex items-center justify-between">
      {/* Left Side: Logo and Title */}
      <div className="flex items-center space-x-2">
        <img src="./icon.png" alt="logo" className="w-7" />
        <h3 className="text-xl font-semibold">
          <span>Talent</span>
          <span className="text-indigo-500">Sync</span>
        </h3>
      </div>

      {/* Right Side: Sign Out Button */}
      {user && (
        <button
          className="bg-red-500 text-white font-semibold px-4 py-2 rounded-lg hover:bg-red-600"
          onClick={signOut}
        >
          Sign Out
        </button>
      )}
    </div>
  );
};

export default Header;
