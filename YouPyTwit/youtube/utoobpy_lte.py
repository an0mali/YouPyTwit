import os
import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
	os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

	api_service_name = "youtube"
	api_version = "v3"
	client_secrets_file = "youtube/yt.config"

    # Get credentials and create an API client
	flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
		client_secrets_file, scopes)
	credentials = flow.run_console()
	youtube = googleapiclient.discovery.build(
		api_service_name, api_version, credentials=credentials)

	request = youtube.search().list(
		part="id,snippet",
		channelId="UCyQPbe7X3Cf7jI1Oa8EG93w",#enter your channel ID code here
		maxResults=50,
		type="video"
		)
	response = request.execute()
	#res = json.loads(response)
	#print(str(res))

	return response
