import { useState } from "react";
import { useAuth } from "../hooks/useAuth";
import { useUser } from "../context/userContext";
import { Loader2, LogIn } from "lucide-react";
import { logError, logInfo } from "../utils/logger";

// Import Chrome Storage utils
import User from "../types/user";
import { getResumeUrl } from "../api/resume";

const Login = () => {
  const { getTokensAndCreds } = useAuth();
  const { setUser } = useUser();
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    logInfo("[Login] Login button pressed!");
    try {
      setLoading(true);
      const { awsCredentials, accessToken } = await getTokensAndCreds();
      if (!accessToken) {
        logInfo("[Login] No accessToken received!");
        return;
      }
      if (!awsCredentials) {
        logInfo("[Login] No aws credentials received!");
        return;
      }

      // fetch user info from google
      const response = await fetch(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        {
          headers: { Authorization: `Bearer ${accessToken}` },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch user information");
      }

      const userInfo = await response.json();
      const resumeUrl = await getResumeUrl(userInfo.email, awsCredentials);

      const user: User = {
        name: userInfo.name,
        email: userInfo.email,
        picture: userInfo.picture,
        resumeUrl: resumeUrl || undefined,
        awsCredentials: awsCredentials,
      };

      setUser(user);
    } catch (error) {
      logError(`[Login] Login failed! ${error}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-[80vh] p-6">
      {/* App Title */}
      <h1 className="text-2xl mb-4 text-center text-gray-900">
        Welcome to
        <span className="flex font-semibold mt-1 items-center justify-center">
          <img src="./icon.png" alt="logo" className="w-7 mr-0" />
          <span>Talent</span>
          <span className="text-indigo-500">Sync</span>!
        </span>
      </h1>

      {/* Description */}
      <p className="text-gray-600 text-sm mb-6 text-center w-64">
        Sign in to start optimizing your job search!
      </p>

      {/* Login Button */}
      <button
        onClick={handleLogin}
        className={`w-52 py-3 flex items-center justify-center gap-2 rounded-lg text-base font-medium transition-all ease-in-out
          ${
            loading
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-500 hover:bg-blue-600 text-white"
          }`}
        disabled={loading}
      >
        {loading ? (
          <>
            <Loader2 className="animate-spin" size={20} />
            Signing in...
          </>
        ) : (
          <>
            <LogIn size={20} />
            Sign in with Google
          </>
        )}
      </button>
    </div>
  );
};

export default Login;
