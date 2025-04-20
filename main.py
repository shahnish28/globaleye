<<<<<<< HEAD
from scraper.config import Config

config = Config()

print(config.MONGODB_URI)
=======
# main.py (root)
from discord.main import main as module1_main
from telegram_scraper.main import main as module2_main
from website_scraper.main import main as module3_main

def main():
    print("=== Starting All Modules ===\n")

    print(">>> Module 1:")
    module1_main()

    print("\n>>> Module 2:")
    module2_main()

    print("\n>>> Module 3:")
    module3_main()

    print("\n=== All Done ===")

if __name__ == "__main__":
    main()
>>>>>>> 70089ca (db connection pending)
