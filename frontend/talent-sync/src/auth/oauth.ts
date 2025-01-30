window.onload = () => {
  const button = document.querySelector("button");

  if (!button) {
    console.error("Button element not found");
    return;
  }

  button.addEventListener("click", () => {
    chrome.identity.getAuthToken({ interactive: true }, (token) => {
      if (chrome.runtime.lastError) {
        console.error(
          "Error fetching auth token:",
          chrome.runtime.lastError.message
        );
        return;
      }

      if (token) {
        console.log("Auth Token:", token);
      } else {
        console.error("No token retrieved");
      }
    });
  });
};
