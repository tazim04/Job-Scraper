// Abstraction for using chrome storage, sends messages to background.js for visible logs

export const setChromeStorage = (key: string, value: any): Promise<void> => {
  return new Promise((resolve, reject) => {
    if (!chrome?.runtime) {
      console.warn("Chrome runtime not available. Are you in an extension?");
      reject(new Error("Chrome runtime not available"));
      return;
    }

    chrome.runtime.sendMessage(
      { action: "setStorage", key, value },
      (response) => {
        if (chrome.runtime.lastError) {
          reject(new Error(chrome.runtime.lastError.message));
        } else {
          console.log(`Stored ${key} successfully:`, value);
          resolve(response?.value ?? null);
        }
      }
    );
  });
};

export const getChromeStorage = (key: string): Promise<any> => {
  return new Promise((resolve, reject) => {
    if (!chrome?.runtime) {
      console.warn("Chrome runtime not available. Are you in an extension?");
      reject(new Error("Chrome runtime not available"));
      return;
    }

    chrome.runtime.sendMessage({ action: "getStorage", key }, (response) => {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
      } else {
        resolve(response?.value ?? null);
      }
    });
  });
};
