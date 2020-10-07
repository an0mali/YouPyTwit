# YouPyTwit
A twitter bot with partial youtube integration that likes, retweets, and composes its own tweets based on configuration files (including hashtags and such) modified by the user. With Youtube integration, the latest 50 videos of the account is pulled to be referenced when composing tweets- current creating a tweet with a link to the video, its title, and (typically) relevant hashtags. The bot operates on a sleep/wake cycle.

To get started: (If you already have a twitter developer account, skip to step 4).
1. Set up your developer account on twitter. Sign in to twitter and go to https://developer.twitter.com/en/apply-for-access
2. Goto developer portal, at the top right click your account name.
3. From the dropdown menu, click apps.
4. Create a new twitter app.
5. From your new app's page, click Keys and tokens.
6. Create a file in the same directory as youpytwit.py called 'consume.aut' and enter your API key on the first line and API secret key on the second line.
7. Also inside this directory, create a file called 'access.aut' and enter your apps access token on the first line and access token secret on the second line.
7. Get your Google developer token for Youtube API (more instructions on this soon), name it 'yt.config' and place it into the youtube directory.
8. Inside this directory, open utoobpy_lte.py and replace the current 'channel id' with your channel's ID.
9. Run youtwitpy.py
