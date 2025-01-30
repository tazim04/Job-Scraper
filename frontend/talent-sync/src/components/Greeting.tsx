import { useUser } from "../context/userContext";

const Greeting = () => {
  const { user } = useUser();

  return (
    <div className="flex flex-col items-center justify-center text-center">
      <img
        src={user?.picture}
        alt="Profile Picture"
        className="rounded-full border-2 border-black w-20 h-20 object-cover"
      />
      <h1 className="text-2xl mt-2">Hi {user?.name}!</h1>
    </div>
  );
};

export default Greeting;
