chrome.runtime.onInstalled.addListener(() => {
  console.log("Extension installed");
});

// Listen for storage-related messages from the frontend
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "setStorage") {
    const { key, value } = request;
    console.log(`Saving ${key} to chrome storage:`, value);

    chrome.storage.local.set({ [key]: value }, () => {
      sendResponse({ status: "success" });
    });
    return true; // Keeps the message channel open for async response
  }

  if (request.action === "getStorage") {
    const { key } = request;
    chrome.storage.local.get([key], (result) => {
      console.log(`Retrieved ${key} from chrome storage:`, result[key]);
      sendResponse({ value: result[key] });
    });
    return true;
  }
});
