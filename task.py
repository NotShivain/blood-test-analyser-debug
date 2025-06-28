from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

from agents import doctor, verifier
from tools import search_tool, blood_test_tool

help_patients = Task(
    description="Analyze blood test report and answer: {query}. Use read_blood_test_report tool.",
    expected_output="Medical analysis with key findings, notable values, and recommendations.",
    agent=doctor,
    tools=[blood_test_tool],
    async_execution=False,
)

nutrition_analysis = Task(
    description="Provide nutrition recommendations based on blood results. Address: {query}",
    expected_output="Nutrition advice including foods to focus on and dietary recommendations.",
    agent=doctor,
    tools=[blood_test_tool],
    async_execution=False,
)

exercise_planning = Task(
    description="Create exercise plan based on blood results. Address: {query}",
    expected_output="Exercise recommendations with types, intensity, and safety considerations.",
    agent=doctor,
    tools=[blood_test_tool],
    async_execution=False,
)

verification = Task(
    description="Verify if document is a valid blood test report.",
    expected_output="Document verification: valid report confirmation and detected markers.",
    agent=doctor,
    tools=[blood_test_tool],
    async_execution=False
)