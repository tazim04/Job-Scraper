import { readFile, writeFile } from "fs/promises";
import { fileURLToPath } from "url";
import { dirname, join } from "path";
import dotenv from "dotenv";

// Load environment variables
dotenv.config();

// Get the current file directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Define paths
const templatePath = join(__dirname, "manifest.template.json");
const manifestPath = join(__dirname, "manifest.json");

try {
  // Read the template file
  let manifest = await readFile(templatePath, "utf8");

  // Replace placeholders with environment variables
  manifest = manifest
    .replace("${KEY}", process.env.KEY || "")
    .replace("${VITE_OAUTH_CLIENT_ID}", process.env.VITE_OAUTH_CLIENT_ID || "")
    .replace("${BACKEND_URL}", process.env.BACKEND_URL || "");

  // Write the new `manifest.json`
  await writeFile(manifestPath, manifest, "utf8");

  console.log("✅ manifest.json generated successfully!");
} catch (error) {
  console.error("❌ Error generating manifest.json:", error);
}
