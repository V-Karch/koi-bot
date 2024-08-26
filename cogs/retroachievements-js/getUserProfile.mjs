// This file will run the api, which is in javascript.
// Pass the username through process.argv[2] and retrieve the webApiKey from gitignored file

// Import libraries
import { buildAuthorization, getUserProfile } from "@retroachievements/api";
import process from 'process';
import fs from 'node:fs';

// Setup authorization variables
const username = "vfk4083"
const searchUsername = process.argv[2];

// Assign webApiKey a value via callback
async function useApiKey(webApiKey) {
    // Create authorization
    const authorization = buildAuthorization({ username, webApiKey });

    // Get user profile
    const userProfile = await getUserProfile(authorization, {username: searchUsername});

    console.log(JSON.stringify(userProfile, null, 2));
}

fs.readFile("api_info.txt", "utf8", (err, data) => {
    if (err) {
        console.error(err);
	return;
    }

    useApiKey(data.trim()); // Send the api key to the callback function
})
