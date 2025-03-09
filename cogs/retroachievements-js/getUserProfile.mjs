// Import libraries
import { buildAuthorization, getUserProfile } from "@retroachievements/api";
import process from 'process';
import fs from 'node:fs';

// Load username from config.json
let username = "";

// Read config.json and extract the "ra-username"
try {
    const configData = fs.readFileSync("config.json", "utf8");
    const config = JSON.parse(configData);
    username = config["ra-username"];
} catch (err) {
    console.error("Error reading config.json:", err);
    process.exit(1);  // Exit if there's an error reading the config file
}

// Retrieve the search username from command line arguments
const searchUsername = process.argv[2];

// Assign webApiKey a value via callback
async function useApiKey(webApiKey) {
    // Create authorization
    const authorization = buildAuthorization({ username, webApiKey });

    // Get user profile
    const userProfile = await getUserProfile(authorization, { username: searchUsername });

    console.log(JSON.stringify(userProfile, null, 2));
}

// Read the API key from the gitignored file "api_info.txt"
fs.readFile("api_info.txt", "utf8", (err, data) => {
    if (err) {
        console.error(err);
        return;
    }

    useApiKey(data.trim()); // Send the API key to the callback function
});

