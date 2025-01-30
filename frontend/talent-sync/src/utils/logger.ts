const LOG_PREFIX = "[TalentSync]";

export const logInfo = (...args: any[]) => {
  console.log(`${LOG_PREFIX} INFO:`, ...args);
  sendLogToBackground("INFO", args);
};

export const logWarn = (...args: any[]) => {
  console.warn(`${LOG_PREFIX} WARNING:`, ...args);
  sendLogToBackground("WARNING", args);
};

export const logError = (...args: any[]) => {
  console.error(`${LOG_PREFIX} ERROR:`, ...args);
  sendLogToBackground("ERROR", args);
};

// Send logs to background.js (only if running in a Chrome extension)
const sendLogToBackground = (level: string, message: any[]) => {
  if (typeof chrome !== "undefined" && chrome.runtime?.sendMessage) {
    chrome.runtime.sendMessage(
      { action: "log", level, message },
      (response) => {
        if (chrome.runtime.lastError) {
          console.warn(
            "[TalentSync] Failed to send log to background.js:",
            chrome.runtime.lastError
          );
        } else {
          console.log(
            "[TalentSync] Log sent to background.js:",
            response?.status
          );
        }
      }
    );
  } else {
    console.warn("[TalentSync] chrome.runtime.sendMessage not available");
  }
};
