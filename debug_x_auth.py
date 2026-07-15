import tweepy
import json
import os

def debug_x_auth():
    with open("x_credentials.json", "r") as f:
        creds = json.load(f)

    print("--- Debugging X Authentication ---")
    
    # Try OAuth 1.0a (v1.1)
    auth = tweepy.OAuthHandler(creds["api_key"], creds["api_secret"])
    auth.set_access_token(creds["access_token"], creds["access_token_secret"])
    api = tweepy.API(auth)

    try:
        user = api.verify_credentials()
        print(f"Success! Authenticated as: @{user.screen_name}")
    except Exception as e:
        print(f"v1.1 Auth Failed: {e}")

    # Try Client (v2)
    client = tweepy.Client(
        consumer_key=creds["api_key"],
        consumer_secret=creds["api_secret"],
        access_token=creds["access_token"],
        access_token_secret=creds["access_token_secret"]
    )

    try:
        # Get own user info via v2
        me = client.get_me()
        if me.data:
            print(f"v2 Auth Success! User ID: {me.data.id}")
        else:
            print("v2 Auth Success, but no data returned.")
    except Exception as e:
        print(f"v2 Auth Failed: {e}")

if __name__ == "__main__":
    debug_x_auth()
