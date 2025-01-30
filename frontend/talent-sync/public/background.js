// Logger utility for background.js
const LOG_PREFIX = "[TalentSync]";

const stringifyArgs = (args) => {
  return args.map((arg) => {
    if (typeof arg === "object") {
      return JSON.stringify(arg, null, 2); // Format objects/arrays
    }
    return arg; // Leave strings/numbers untouched
  });
};

const logInfo = (...args) => {
  const formattedArgs = stringifyArgs(args);
  console.log(`${LOG_PREFIX} INFO:`, ...formattedArgs);
};

const logWarn = (...args) => {
  const formattedArgs = stringifyArgs(args);
  console.warn(`${LOG_PREFIX} WARNING:`, ...formattedArgs);
};

const logError = (...args) => {
  const formattedArgs = stringifyArgs(args);
  console.error(`${LOG_PREFIX} ERROR:`, ...formattedArgs);
};

// Listen for extension installation
chrome.runtime.onInstalled.addListener(() => {
  logInfo("Extension installed or updated.");
});

// Listen for messages from the frontend (popup or content scripts)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  logInfo("Received message:", request);

  if (request.action === "setStorage") {
    const { key, value } = request;
    logInfo(`Saving ${key} to chrome storage:`, value);

    chrome.storage.local.set({ [key]: value }, () => {
      logInfo(`Successfully saved ${key}`);
      sendResponse({ status: "success" });
    });
    return true; // Keeps the message channel open for async response
  }

  if (request.action === "getStorage") {
    const { key } = request;
    chrome.storage.local.get([key], (result) => {
      logInfo(`Retrieved ${key} from chrome storage:`, result[key]);
      sendResponse({ value: result[key] });
    });
    return true;
  }

  if (request.action === "log") {
    logInfo("LOG from popup:", request.message);
    sendResponse({ status: "logged" });
    return true;
  }
});
