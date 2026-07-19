"""
One-time script to populate the ChromaDB database
using facts from data/sports_facts.json.

Run this script once before starting the application.
"""

from src.database import populate_database


def main():
    print("=" * 50)
    print("Initializing ChromaDB...")
    print("=" * 50)

    populate_database()

    print("=" * 50)
    print("Database setup completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()