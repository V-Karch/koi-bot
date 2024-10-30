// Import libraries
import { buildAuthorization, getGameInfoAndUserProgress } from "@retroachievements/api";
import process from "process";
import fs from "node:fs";

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

// Retrieve the search username and game ID from command line arguments
const searchUsername = process.argv[2];
const searchGameId = process.argv[3];

// Assign webApiKey a value via callback
async function useApiKey(webApiKey) {
    // Create authorization
    const authorization = buildAuthorization({ username, webApiKey });
    
    // Get Game Info and User Progress
    const gameInfoAndUserProgress = await getGameInfoAndUserProgress(authorization, {
        username: searchUsername,
        gameId: searchGameId,
    });

    console.log(JSON.stringify(gameInfoAndUserProgress, null, 2));
}

// Read the API key from the gitignored file "api_info.txt"
fs.readFile("api_info.txt", "utf8", (err, data) => {
    if (err) {
        console.error(err);
        return;
    }

    useApiKey(data.trim()); // Send the API key to the callback function
});
