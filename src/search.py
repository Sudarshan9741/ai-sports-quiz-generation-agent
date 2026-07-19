from duckduckgo_search import DDGS


def get_live_news_context(sport_name: str) -> str:
    """
    Fetch recent sports news using DuckDuckGo.
    Returns a single text block containing the top results.
    """

    search_query = (
        f"{sport_name} latest tournament "
        f"results championship winners news"
    )

    snippets = []

    try:
        with DDGS() as ddgs:

            results = ddgs.text(
                keywords=search_query,
                max_results=3,
            )

            for index, result in enumerate(results, start=1):

                title = result.get("title", "No Title")

                body = result.get(
                    "body",
                    "No Description Available",
                )

                snippets.append(
                    f"Source {index}\n"
                    f"Title: {title}\n"
                    f"{body}"
                )

    except Exception as error:

        return (
            "Unable to retrieve live sports news.\n"
            f"Reason: {error}"
        )

    return "\n\n".join(snippets)