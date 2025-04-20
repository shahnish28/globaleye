import time
from discum import Client

TOKEN = "MTMyMDc2MTE1NzE1NzM4ODMxMw.GGxTfJ.tNS4QUO4QzdNwjsuoLm5FmmS6JrmZrdiyKfPNg"
GUILD_ID = "695622741298249748"
CHANNEL_ID = "695627736819040298"

bot = Client(token=TOKEN, log=False)

@bot.gateway.command
def on_ready(resp):
    if resp.event.ready_supplemental:
        print("Logged in successfully!")
        time.sleep(5)  # Give some time for the session to initialize
        bot.gateway.fetchMembers(GUILD_ID, CHANNEL_ID)

bot.gateway.run(auto_reconnect=True)
