import { useUser } from "../context/userContext";

const Greeting = () => {
  const { user } = useUser();
  return (
    <div>
      <img
        src={user?.picture}
        alt="Profile Picture"
        className="rounded-full border-2 border-black"
      />
      <h1 className="text-2xl">Hi {user?.name}!</h1>
    </div>
  );
};

export default Greeting;
