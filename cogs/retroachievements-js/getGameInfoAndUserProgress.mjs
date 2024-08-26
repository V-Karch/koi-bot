// This file will run the api, which is in javascript
// Pass the username and gave id through process.argv[2] and process.argv[3] respectively

import { buildAuthorization, getGameInfoAndUserProgress } from "@retroachievements/api";
import process from "process";
import fs from "node:fs";

// Setup authorization variables
const username = "vfk4083";
const searchUsername = process.argv[2];
const searchGameId = process.argv[3];

// Assign webApiKey a value via callback
async function useApiKey(webApiKey) {
    // Create authorization
    const authorization = buildAuthorization({username, webApiKey});
    
    // Get Game Info and User Progress
    const gameInfoAndUserProgress = await getGameInfoAndUserProgress(authorization, {
	    username: searchUsername,
	    gameId: searchGameId,
    });

    console.log(JSON.stringify(gameInfoAndUserProgress, null, 2));
}

fs.readFile("api_info.txt", "utf8", (err, data) => {
    if (err) {
        console.error(err);
	return;
    }

    useApiKey(data.trim());
});
