import random

from google import genai

from src.config import GEMINI_API_KEY, GEMINI_MODEL
from src.database import query_database
from src.search import get_live_news_context

# -----------------------------------------
# Gemini Client
# -----------------------------------------
client = genai.Client(api_key=GEMINI_API_KEY)


# -----------------------------------------
# Generate Quiz
# -----------------------------------------
def generate_quiz(sport: str, difficulty: str) -> str:
    """
    Generate a sports quiz using:
    1. Historical facts from ChromaDB
    2. Latest sports news from DuckDuckGo
    3. Gemini AI
    """

    # -----------------------------------------
    # Historical Context (RAG)
    # -----------------------------------------
    historical_facts = query_database(
        sport=sport,
        query=f"{sport} history records championships famous players",
        n_results=5,
    )

    historical_context = "\n".join(historical_facts)

    # -----------------------------------------
    # Latest Sports News
    # -----------------------------------------
    live_context = get_live_news_context(sport)

    # -----------------------------------------
    # Random Quiz ID
    # -----------------------------------------
    random_seed = random.randint(100000, 999999)

    # -----------------------------------------
    # Prompt
    # -----------------------------------------
    prompt = f"""
You are an expert Sports Quiz Generator.

Quiz ID:
{random_seed}

Generate EXACTLY FIVE multiple-choice questions.

Sport:
{sport}

Difficulty:
{difficulty}

Every time this prompt is executed, generate a completely NEW quiz.

Never repeat:
- Questions
- Players
- Venues
- Records
- Championships
- Statistics
- News topics
- Wording

Each quiz should feel completely different from previous generations.

=========================================================
DIFFICULTY RULES
=========================================================

Easy

• Beginner friendly
• Famous players
• Famous tournaments
• Basic rules
• Popular records
• Easy historical facts

Medium

• Historical events
• Championships
• Famous venues
• Player achievements
• Moderate reasoning
• Mix historical facts with recent news
• Never repeat Easy questions

Hard

• Advanced reasoning
• Historical + Live News
• Rankings
• Statistics
• Comparisons
• Challenging questions
• Never repeat Easy or Medium questions

=========================================================
QUESTION DISTRIBUTION
=========================================================

Easy
4 Historical
1 Latest News

Medium
3 Historical
2 Latest News

Hard
2 Historical
3 Latest News

=========================================================
IMPORTANT RULES
=========================================================

1. Generate EXACTLY FIVE questions.

2. Every question must be unique.

3. Never repeat a topic.

4. Never repeat a question from previous generations.

5. Randomize question order.

6. Randomize the correct answer position.
The answer should sometimes be:

A
B
C
D

Do NOT always use A.

7. Use different players, venues, championships,
records, rules, rankings and news every time.

8. Every option must belong to the SAME category.

Example

Player Question

A) Virat Kohli
B) Rohit Sharma
C) Joe Root
D) Steve Smith

Year Question

A) 1983
B) 1992
C) 2007
D) 2011

Venue Question

A) Lord's
B) MCG
C) Eden Gardens
D) Wankhede

Never mix categories.

=========================================================
QUESTION TOPICS
=========================================================

Randomly choose from topics like

• World Cups
• Championships
• Famous Players
• Captains
• Coaches
• Stadiums
• Records
• Rankings
• Awards
• Rules
• Legendary Matches
• Women's Sports
• Olympic History
• Latest News

Every quiz should contain a different combination of topics.
=========================================================
OUTPUT FORMAT
=========================================================

Follow EXACTLY this format.

Question 1

<Question>

A) Option One

B) Option Two

C) Option Three

D) Option Four

Correct Answer:
A) Option One

Explanation:
<One concise explanation>

Repeat the same format for all FIVE questions.

Return ONLY the quiz.

=========================================================
HISTORICAL FACTS
=========================================================

{historical_context}

=========================================================
LATEST SPORTS NEWS
=========================================================

{live_context}
"""

    # -----------------------------------------
    # Gemini Response
    # -----------------------------------------
    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        if not response.text:
            return "Error: Gemini returned an empty response."

        quiz = response.text.strip()

        # -----------------------------------------
        # Format Options
        # -----------------------------------------

        quiz = quiz.replace("\r", "")

        quiz = quiz.replace(" A)", "\nA)")
        quiz = quiz.replace(" B)", "\nB)")
        quiz = quiz.replace(" C)", "\nC)")
        quiz = quiz.replace(" D)", "\nD)")

        quiz = quiz.replace("Correct Answer:", "\nCorrect Answer:")
        quiz = quiz.replace("Explanation:", "\nExplanation:")

        return quiz

    except Exception as error:
        return f"Error: {error}"