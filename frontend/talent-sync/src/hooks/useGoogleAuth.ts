// Hook to retrieve google auth token

export const useGoogleAuth = () => {
  const getAuthToken = async (): Promise<string | null> => {
    return new Promise((resolve, reject) => {
      if (!chrome?.identity) {
        reject("Chrome identity API is not available.");
        return;
      }

      chrome.identity.getAuthToken({ interactive: true }, (token) => {
        if (chrome.runtime.lastError) {
          reject(chrome.runtime.lastError.message);
        } else if (token) {
          resolve(token);
        } else {
          reject("No token retrieved");
        }
      });
    });
  };

  return { getAuthToken };
};
