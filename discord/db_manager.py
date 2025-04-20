import psycopg2
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection details
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

def connect_db():
    """Establish and return a database connection."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"[ERROR] Database connection error: {e}")
        return None

def create_tables():
    """Create tables for storing channels and messages if they don't exist."""
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cur:
                # Create channels table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS channels (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL
                    );
                """)
                
                # Create messages table with JSONB support
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id TEXT PRIMARY KEY,  -- Message ID
                        channel_id TEXT NOT NULL,
                        author_id TEXT,
                        author_username TEXT,
                        content TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        reactions JSONB,
                        embeds JSONB,
                        components JSONB,
                        FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE
                    );
                """)
                conn.commit()
                print("[INFO] Tables created successfully.")
        except Exception as e:
            print(f"[ERROR] Error creating tables: {e}")
        finally:
            conn.close()

def store_channel(channel_id, channel_name):
    """Insert or update a channel record in the database."""
    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO channels (id, name)
                    VALUES (%s, %s)
                    ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
                """, (channel_id, channel_name))
                conn.commit()
                print(f"[INFO] Channel {channel_id} stored.")
        except Exception as e:
            print(f"[ERROR] Error storing channel: {e}")
        finally:
            conn.close()

def store_message(channel_id, messages):
    """Insert multiple messages into the database."""
    if not messages:
        print("[WARNING] No messages to store.")
        return

    conn = connect_db()
    if conn:
        try:
            with conn.cursor() as cur:
                for msg in messages:
                    msg_id = msg.get("id")
                    if not msg_id:
                        print(f"[WARNING] Skipping message with missing ID: {msg}")
                        continue

                    author_id = msg.get("author", {}).get("id", None)
                    author_username = msg.get("author", {}).get("username", None)
                    content = msg.get("content", "")
                    timestamp = msg.get("timestamp", None)
                    reactions = json.dumps(msg.get("reactions", []))
                    embeds = json.dumps(msg.get("embeds", []))
                    components = json.dumps(msg.get("components", []))

                    print(f"[DEBUG] Storing Message ID: {msg_id}, Content: {content}")

                    cur.execute("""
                        INSERT INTO messages (id, channel_id, author_id, author_username, content, timestamp, reactions, embeds, components)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO UPDATE SET 
                            content = EXCLUDED.content,
                            timestamp = EXCLUDED.timestamp;
                    """, (msg_id, channel_id, author_id, author_username, content, timestamp, reactions, embeds, components))
                
                conn.commit()
                print(f"[INFO] Stored {len(messages)} messages for channel {channel_id}.")
        except Exception as e:
            print(f"[ERROR] Error storing messages: {e}")
        finally:
            conn.close()

# Create the tables when script is executed
create_tables()
