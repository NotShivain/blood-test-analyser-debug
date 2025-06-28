## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()
from litellm import completion

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

from tools import search_tool, blood_test_tool

### Loading LLM
import os
llm = LLM(
    api_key=os.getenv("GROQ_API_KEY"),
    model="groq/llama-3.1-8b-instant",
)

# Creating an Experienced Doctor agent
doctor=Agent(
    role="Senior Medical Doctor and Blood Test Specialist",
    goal="Analyze blood test reports and provide accurate medical insights for: {query}",
    verbose=False,
    memory=False,
    backstory="Senior medical doctor specializing in blood test interpretation and clinical pathology.",
    tools=[blood_test_tool],
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)
verifier = Agent(
    role="Medical Document Validator",
    goal="Verify that uploaded documents are valid blood test reports and ensure data quality.",
    verbose=False,
    memory=False,
    backstory="Medical records specialist with expertise in laboratory report validation.",
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)


nutritionist = Agent(
    role="Clinical Nutritionist and Dietitian",
    goal="Provide evidence-based nutrition recommendations based on blood test results.",
    verbose=False,
    memory=False,
    backstory="Registered dietitian specializing in clinical nutrition and laboratory medicine analysis.",
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)


exercise_specialist = Agent(
    role="Clinical Exercise Physiologist",
    goal="Recommend safe, evidence-based exercise plans tailored to blood test results and health status.",
    verbose=False,
    memory=False,
    backstory=(
        "You are a certified clinical exercise physiologist with expertise in exercise prescription for medical conditions. "
        "You analyze blood biomarkers to assess cardiovascular health, metabolic function, and fitness capacity. "
        "You design personalized exercise programs that consider medical contraindications and individual health status. "
        "Your recommendations prioritize safety while maximizing health benefits through appropriate physical activity."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)
