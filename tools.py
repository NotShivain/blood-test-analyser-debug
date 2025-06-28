import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from langchain_community.document_loaders import PyPDFLoader

search_tool = None

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class BloodTestReportInput(BaseModel):
    path: str = Field(default='data/sample.pdf', description="Path of the pdf file to read")

class BloodTestReportTool(BaseTool):
    name: str = "read_blood_test_report"
    description: str = "Tool to read data from a blood test report PDF file from a path"
    args_schema: Type[BaseModel] = BloodTestReportInput

    def _run(self, path: str = 'data/sample.pdf') -> str:
        docs = PyPDFLoader(file_path=path).load()

        full_report = ""
        for data in docs:
            content = data.page_content
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
            full_report += content + "\n"
        
        max_chars = 6000
        if len(full_report) > max_chars:
            full_report = full_report[:max_chars] + "\n... [Content truncated to fit token limits]"
            
        return full_report

blood_test_tool = BloodTestReportTool()

## Creating Nutrition Analysis Tool
class NutritionTool:
    @staticmethod
    async def analyze_nutrition_tool(blood_report_data):
        processed_data = blood_report_data
        
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
                
        nutrition_recommendations = []
        
        if "vitamin d" in processed_data.lower() or "25-oh" in processed_data.lower():
            nutrition_recommendations.append("Consider vitamin D supplementation and sun exposure")
        
        if "b12" in processed_data.lower() or "cobalamin" in processed_data.lower():
            nutrition_recommendations.append("Include B12-rich foods: meat, fish, dairy, fortified cereals")
        
        if "iron" in processed_data.lower() or "ferritin" in processed_data.lower():
            nutrition_recommendations.append("Iron-rich foods: lean meats, spinach, lentils, fortified cereals")
        
        if "cholesterol" in processed_data.lower():
            nutrition_recommendations.append("Heart-healthy diet: omega-3 fatty acids, fiber-rich foods, limit saturated fats")
        
        if "glucose" in processed_data.lower() or "hba1c" in processed_data.lower():
            nutrition_recommendations.append("Blood sugar management: complex carbs, fiber, regular meals")
        
        if "calcium" in processed_data.lower():
            nutrition_recommendations.append("Calcium sources: dairy, leafy greens, fortified plant milks")
        
        if not nutrition_recommendations:
            nutrition_recommendations.append("Maintain balanced diet with fruits, vegetables, whole grains, lean proteins")
        
        return "\n".join(nutrition_recommendations)

## Creating Exercise Planning Tool
class ExerciseTool:
    @staticmethod
    async def create_exercise_plan_tool(blood_report_data):
        exercise_recommendations = []
        
        data_lower = blood_report_data.lower()
        
        if "cholesterol" in data_lower or "ldl" in data_lower:
            exercise_recommendations.append("Cardiovascular exercise: 150 min/week moderate intensity")
            exercise_recommendations.append("Activities: brisk walking, cycling, swimming")
        
        if "glucose" in data_lower or "diabetes" in data_lower:
            exercise_recommendations.append("Blood sugar control: mix of aerobic and resistance training")
            exercise_recommendations.append("Post-meal walks to help glucose management")
        
        if "blood pressure" in data_lower or "hypertension" in data_lower:
            exercise_recommendations.append("Low-impact aerobic exercise to reduce blood pressure")
            exercise_recommendations.append("Avoid heavy weightlifting, focus on moderate resistance")
        
        if "vitamin d" in data_lower:
            exercise_recommendations.append("Outdoor activities for natural vitamin D synthesis")
            exercise_recommendations.append("Weight-bearing exercises for bone health")
        
        if "iron" in data_lower or "anemia" in data_lower:
            exercise_recommendations.append("Start with low-intensity exercise, gradually increase")
            exercise_recommendations.append("Monitor fatigue levels during workouts")
        
        if not exercise_recommendations:
            exercise_recommendations.append("General fitness: 150 min moderate aerobic + 2 days strength training")
            exercise_recommendations.append("Include flexibility and balance exercises")
        
        exercise_recommendations.append("Consult healthcare provider before starting new exercise program")
        
        return "\n".join(exercise_recommendations)

nutrition_tool = NutritionTool()
exercise_tool = ExerciseTool()