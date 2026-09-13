import os
from dotenv import load_dotenv
from agents import Agent, Runner, SQLiteSession

load_dotenv()

session = SQLiteSession("career_agent_session")

agent = Agent(
    name="Career Agent",
    instructions="""
You are an AI Career Assistant for students.

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
)


while True:
    user_input = input("\nYou: ")

    if any(word in user_input.lower().split() for word in ["bye", "goodbye", "exit", "quit"]):
        print("Career Agent: Goodbye! Good luck with your career journey.")
        break

    result = Runner.run_sync(agent, user_input, session=session)

    print("\nCareer Agent:", result.final_output)