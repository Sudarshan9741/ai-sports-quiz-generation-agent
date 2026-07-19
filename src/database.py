import json
import os

import chromadb

from src.config import CHROMA_DB_PATH, SPORTS_DATA_PATH


def get_chroma_client():
    """
    Create and return a persistent ChromaDB client.
    """
    return chromadb.PersistentClient(path=CHROMA_DB_PATH)


def get_collection():
    """
    Get or create the ChromaDB collection.
    """

    client = get_chroma_client()

    return client.get_or_create_collection(
        name="sports_history"
    )


def populate_database():
    """
    Load sports facts from JSON into ChromaDB.
    """

    collection = get_collection()

    if collection.count() > 0:
        print(f"Database already contains {collection.count()} facts.")
        return

    if not os.path.exists(SPORTS_DATA_PATH):
        raise FileNotFoundError(
            f"Sports facts file not found: {SPORTS_DATA_PATH}"
        )

    with open(SPORTS_DATA_PATH, "r", encoding="utf-8") as file:
        facts = json.load(file)

    documents = []
    metadatas = []
    ids = []

    for index, item in enumerate(facts):
        documents.append(item["fact"])
        metadatas.append({"sport": item["sport"]})
        ids.append(f"fact_{index}")

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
    )

    print(f"Successfully stored {len(documents)} facts.")


def query_database(
    sport: str,
    query: str,
    n_results: int = 3,
):
    """
    Retrieve relevant facts for a sport.
    """

    collection = get_collection()

    results = collection.query(
        query_texts=[query],
        where={"sport": sport},
        n_results=n_results,
    )

    if (
        "documents" not in results
        or results["documents"] is None
        or len(results["documents"]) == 0
    ):
        return []

    return results["documents"][0]