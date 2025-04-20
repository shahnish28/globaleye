# import discum
# import json
# import os
# import hashlib
# from db_manager import store_channel  # Import the database function

# TOKEN = "MTMyMDc2MTE1NzE1NzM4ODMxMw.GGxTfJ.tNS4QUO4QzdNwjsuoLm5FmmS6JrmZrdiyKfPNg"
# GUILD_ID = "896716443880656936"
# CACHE_DIR1 = "channel_cache"
# CACHE_DIR = os.path.join(CACHE_DIR1, "channels")

# bot = discum.Client(token=TOKEN, log=True)  # Enable logs for debugging

# # Ensure the cache directory exists
# if not os.path.exists(CACHE_DIR):
#     os.makedirs(CACHE_DIR)

# def hash_id(channel_id):
#     """Generate a unique hash for a given channel ID."""
#     return hashlib.sha256(channel_id.encode()).hexdigest()

# def load_cache(channel_id):
#     """Load cached data for a specific channel if available."""
#     hashed_id = hash_id(channel_id)
#     file_path = os.path.join(CACHE_DIR, f"{hashed_id}.json")
    
#     if os.path.exists(file_path):
#         with open(file_path, "r") as f:
#             return json.load(f)
#     return None

# def save_cache(channel_id, channel_name):
#     """Save channel data to a uniquely named file."""
#     hashed_id = hash_id(channel_id)
#     file_path = os.path.join(CACHE_DIR, f"{hashed_id}.json")
    
#     data = {"id": channel_id, "name": channel_name}
#     with open(file_path, "w") as f:
#         json.dump(data, f, indent=4)

# @bot.gateway.command
# def get_channels(resp):
#     if resp.event.ready_supplemental:  # Ensure bot is connected
#         print("Bot is connected!")

#         try:
#             data = bot.getGuildChannels(GUILD_ID).json()
#             if not data:
#                 print("No channels found or request failed!")
#                 return

#             new_channels_detected = False

#             for channel in data:
#                 channel_id = channel["id"]
#                 channel_name = channel["name"]

#                 cached_data = load_cache(channel_id)
                
#                 if cached_data and cached_data["name"] == channel_name:
#                     print(f"Cached: {channel_name} ({channel_id})")
#                     # store_channel(channel_id,channel_name)
#                 else:
#                     print(f"New/Updated: {channel_name} ({channel_id})")
#                     save_cache(channel_id, channel_name)  # Save to cache
#                     store_channel(channel_id, channel_name)  # Save to database
#                     new_channels_detected = True

#             if not new_channels_detected:
#                 print("No new channels detected. Using cached data.")

#         except Exception as e:
#             print(f"Error fetching channels: {e}")

#         bot.gateway.close()

# bot.gateway.run()
import discum
import json
import os
import hashlib
# from db_manager import store_channel  # Import the database function

TOKEN = "MTMyMDc2MTE1NzE1NzM4ODMxMw.GGxTfJ.tNS4QUO4QzdNwjsuoLm5FmmS6JrmZrdiyKfPNg"
GUILD_ID = "896716443880656936"
CACHE_DIR1 = "channel_cache"
CACHE_DIR = os.path.join(CACHE_DIR1, "channels")

bot = discum.Client(token=TOKEN, log=True)  # Enable logs for debugging

# Ensure the cache directory exists
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def hash_id(channel_id):
    return hashlib.sha256(channel_id.encode()).hexdigest()

def load_cache(channel_id):
    hashed_id = hash_id(channel_id)
    file_path = os.path.join(CACHE_DIR, f"{hashed_id}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return None

def save_cache(channel_id, channel_name):
    hashed_id = hash_id(channel_id)
    file_path = os.path.join(CACHE_DIR, f"{hashed_id}.json")
    data = {"id": channel_id, "name": channel_name}
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def main():
    @bot.gateway.command
    def get_channels(resp):
        if resp.event.ready_supplemental:
            print("Bot is connected!")
            try:
                data = bot.getGuildChannels(GUILD_ID).json()
                if not data:
                    print("No channels found or request failed!")
                    return

                new_channels_detected = False
                for channel in data:
                    channel_id = channel["id"]
                    channel_name = channel["name"]
                    cached_data = load_cache(channel_id)

                    if cached_data and cached_data["name"] == channel_name:
                        print(f"Cached: {channel_name} ({channel_id})")
                    else:
                        print(f"New/Updated: {channel_name} ({channel_id})")
                        save_cache(channel_id, channel_name)
                        store_channel(channel_id, channel_name)
                        new_channels_detected = True

                if not new_channels_detected:
                    print("No new channels detected. Using cached data.")
            except Exception as e:
                print(f"Error fetching channels: {e}")

            bot.gateway.close()

    bot.gateway.run()

# So it runs only when executed directly
if __name__ == "__main__":
    main()
