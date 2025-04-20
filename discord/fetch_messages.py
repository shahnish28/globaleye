import discum
import json
import os
import hashlib
# from db_manager import store_message  # Ensure your db_manager.py has this function

TOKEN = "MTMyMDc2MTE1NzE1NzM4ODMxMw.GGxTfJ.tNS4QUO4QzdNwjsuoLm5FmmS6JrmZrdiyKfPNg"
GUILD_ID = "896716443880656936"
CACHE_DIR = "channel_cache"
CHANNELS_DIR = os.path.join(CACHE_DIR, "channels")
MESSAGES_DIR = os.path.join(CACHE_DIR, "messages")

# Ensure directories exist
os.makedirs(CHANNELS_DIR, exist_ok=True)
os.makedirs(MESSAGES_DIR, exist_ok=True)

bot = discum.Client(token=TOKEN, log=True)


def hash_id(channel_id):
    """Generate a unique hash for a given channel ID."""
    return hashlib.sha256(channel_id.encode()).hexdigest()


def get_cache_filename(channel_id, is_messages=True):
    """Generate cache file path for a given channel ID."""
    subdir = MESSAGES_DIR if is_messages else CHANNELS_DIR
    return os.path.join(subdir, f"{hash_id(channel_id)}.json")


def load_channel_ids():
    """Load channel IDs from hashed channel files."""
    channel_ids = []
    for filename in os.listdir(CHANNELS_DIR):
        file_path = os.path.join(CHANNELS_DIR, filename)
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                if "id" in data:
                    channel_ids.append(data["id"])
        except Exception as e:
            print(f"Error reading {filename}: {e}")
    return channel_ids


def save_to_cache(channel_id, data, is_messages=True):
    """Save messages or channels to a cache file."""
    cache_file = get_cache_filename(channel_id, is_messages)
    with open(cache_file, "w") as f:
        json.dump(data, f, indent=4)


def load_from_cache(channel_id, is_messages=True):
    """Load data from cache if available."""
    cache_file = get_cache_filename(channel_id, is_messages)
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    return None


def fetch_and_cache_messages():
    """Core logic to fetch messages and save to cache."""
    channel_ids = load_channel_ids()
    if not channel_ids:
        print("No channel IDs found.")
        return

    for channel_id in channel_ids:
        cached_messages = load_from_cache(channel_id)
        if cached_messages:
            print(f"Using cached messages for Channel {channel_id}")
            # Uncomment this if you want to store in DB as well
            # store_message(channel_id, cached_messages)
        else:
            try:
                messages = bot.getMessages(channel_id, num=100).json()
                print(f"Fetched {len(messages)} messages for Channel {channel_id}")
                save_to_cache(channel_id, messages)
                # store_message(channel_id, messages)
            except Exception as e:
                print(f"Error fetching messages for {channel_id}: {e}")


@bot.gateway.command
def on_ready(resp):
    if resp.event.ready_supplemental:
        print("Logged in successfully! Fetching messages...")
        fetch_and_cache_messages()
        bot.gateway.close()


def main():
    bot.gateway.run()


if __name__ == "__main__":
    main()
