# Sample apps for Uminal

This repository implements 3 of the sample applications shown in the Uminal demo video:

- Web search
  - Uses the SerpApi to search Google
- Database
  - Answers the input question by performing operations on a database, using an LLM.
- LLM math
  - Converts the natural language input into Python code that produces an accurate answer, using an LLM.

All of these are implemented in the `app.py` file.

Fun fact: As you can see from the code, these apps are actually just a few [**Langchain**](https://github.com/hwchase17/langchain) Chains, wrapped around an API endpoint!

**Key point:** As long as an app has an API endpoint that can read/write text, it can plug into Uminal and start composing w/ all of the other apps, automatically.

## Integrating these apps w/ Uminal
To add these apps to Uminal, you would first have to deploy this `Flask` app behind a public API endpoint. I've personally used AWS Lambda, but the specific provider doesn't matter here. 

For now, let's just say that this `Flask` API is running at `https://myapps.com`.

Here's how we would add the **Web search** app to Uminal:

In Uminal's web interface, go to the **Apps** page, and click on the ***Add app*** button.

Give the app a descriptive name/description (so that other users can easily find & install your app, if it's public), and then add a new ***Action***.

### Actions
**Actions** basically represent "skills" in Uminal. 

Each action should have the following:
- a name describing what it does (e.g., for our **Web search** app, it could just be "Search")
- when Uminal should use this app (e.g., "Useful for when you need to answer questions about current events.")
- the webhook URL that Uminal should use to interact with the app (in our case, it would be: https://myapps.com/api/web_search)

Apps can define multiple actions, but for our sample *Web search* app, we only need to define the "Search" action, as described in the bullet points above.

### User configurations
In addition to **Actions**, Uminal apps can also define **User configurations**. 

Since the same apps can be shared with/installed by multiple other Uminal users, it would be nice if the apps could ask their users for certain configuration information (such as their username within the app, an API key, etc.) at the time of installation. 

This is what **User configurations** are for.

Once a user configures an app & adds it to their account, Uminal will automatically include the user's provided configuration values within any API requests it makes to your app's API endpoints. This way, your apps can customize their runtime behavior based on the end user that Uminal is invoking your app for.

For our web search app, we can just leave the **User configurations** list empty, and create the app.


Once the app has been created, enable it on the app page.

Congrats, you've essentially just granted GPT-3 new capabilities to search the internet!

Now, you should be able to try prompts like "What is the weather in San Diego like?", and get back reasonable responses (since Uminal would use Google to get the real-time weather forecast, as opposed to just letting GPT-3 generate inaccurate, but reasonably sounding text).

In fact, this makes me wonder: you could even build a Uminal app for getting accurate weather info from a Weather API! This way, you could teach Uminal to use the specialized Weather API for getting weather-related information, as opposed to relying on generic Google searching. 

And you could have both of these apps enabled, so that Uminal could use both of them as needed when responding to your prompts!

## Help
If you have any questions/comments/feedback (or just want early access to the things we'll be shipping), join our Discord (https://discord.gg/qczbX5rzD8) and we'd be happy to help! :D

We can't wait to see what you'll build on top of Uminal!

Onwards! 🚀