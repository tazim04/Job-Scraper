import { useGoogleAuth } from "../hooks/useGoogleAuth";
import { useUser } from "../context/userContext";
import { useNavigate } from "../hooks/useNavigate";

// Import Chrome Storage utils
import User from "../types/user";

const Login = () => {
  const { navigate } = useNavigate();
  const { getAuthToken } = useGoogleAuth();
  const { setUser } = useUser();

  const handleLogin = async () => {
    try {
      const token = await getAuthToken();
      if (!token) return;

      const response = await fetch(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        {
          method: "GET",
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch user information");
      }

      const userInfo = await response.json();

      const userData: User = {
        name: userInfo.name,
        email: userInfo.email,
        picture: userInfo.picture,
      };

      setUser(userData);

      navigate("dashboard", "upload");
    } catch (error) {
      console.error("Login failed:", error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-[80vh]">
      <h1 className="text-2xl mb-4 text-center">
        Welcome to
        <span className="flex font-semibold mt-1">
          <img src="./icon.png" alt="logo" className="w-7" />
          <span>Talent</span>
          <span className="text-emerald-500">Sync</span>!
        </span>
      </h1>
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
        onClick={handleLogin}
      >
        Sign in with Google
      </button>
    </div>
  );
};

export default Login;
