const JobScanner = () => {
  const handleScanJob = async () => {
    console.log("Fetching job details...");
    // TODO: Call backend to scrape the open job
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-2xl mb-4">Job Scanner</h1>
      <button
        onClick={handleScanJob}
        className="bg-purple-500 text-white px-4 py-2 rounded"
      >
        Scan Job
      </button>
    </div>
  );
};

export default JobScanner;
