
# coding: utf-8

# In[1]:


import os
import time
import re,config
from slackclient import SlackClient
import assistant

# instantiate Slack client
slack_client = SlackClient(config.slackbot)
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        print(event)
        if event["type"] == "message" and not "subtype" in event:
            message =event["text"]
            return message, event["channel"],event['user']
    return None, None,None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel,user):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    global assistant
    response=assistant.message(command,channel,user)
    # Sends the response back to the channel
    if isinstance(response, list):
        for r in response:
            slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=r 
    )

def getUser(uid):
    t=slack_client.api_call("users.info",user=uid)
    return  t['user']['profile']['display_name']
# In[2]:


if __name__ == "__main__":
    assistant.registerUserMethod(getUser)
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel,user = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel,user)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

