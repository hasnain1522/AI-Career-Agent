import os
from dotenv import load_dotenv
from agents import Agent, Runner, SQLiteSession, function_tool

load_dotenv()

session = SQLiteSession("career_agent_session")

@function_tool
def get_career_roadmap(career: str) -> str:
    """Provides a basic learning roadmap for a specific career."""

    print("🔥")

    if career.lower() == "ai engineer":
        return """
AI Engineer Roadmap:

1. Python
2. Data Structures & Algorithms
3. Mathematics for AI/ML
4. NumPy, Pandas and Matplotlib
5. Machine Learning
6. Deep Learning
7. Transformers and LLMs
8. APIs and FastAPI
9. Docker and deployment
10. AI projects and portfolio
"""

    return f"No specific roadmap is available yet for {career}."
agent = Agent(
    name="Career Agent",
    instructions="""
You are an AI Career Assistant for students.

When a user asks for a career roadmap,if needed use the
get_career_roadmap tool to obtain the roadmap
instead of creating the roadmap yourself.

Your job is to help users with:
- Career planning
- Career paths
- Skills
- Learning roadmaps
- AI/ML careers
- Programming careers
- Internship preparation
- Resume preparation
- Interview preparation
- Project ideas
- Technical learning

IMPORTANT:
Only answer questions related to education, careers,
skills, internships, resumes, interviews, projects,
programming, AI/ML, and learning.

If the user asks something outside these areas,
do NOT answer that question.

Instead, politely say:

"I'm a Career Agent and I'm not programmed to
handle that type of question. I can help you with
careers, skills, learning, internships, resumes,
interviews, and projects."

Keep your answers practical and easy to understand.
""",
    tools=[get_career_roadmap],
)


while True:
    user_input = input("\nYou: ")

    if any(word in user_input.lower().split() for word in ["bye", "goodbye", "exit", "quit"]):
        print("Career Agent: Goodbye! Good luck with your career journey.")
        break

    result = Runner.run_sync(agent, user_input, session=session)

    print("\nCareer Agent:", result.final_output)