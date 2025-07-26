"""
Enhanced CrewAI with Multi-LLM Support and Rate Limit Bypass
"""

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from .tools import SearchTool, NewsSearchTool
from .llm_manager import get_dynamic_llm_config, initialize_llm_manager
import os

@CrewBase
class EnhancedFirstcrew():
    """Enhanced Firstcrew with multi-LLM support"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        super().__init__()
        # Initialize the LLM manager
        initialize_llm_manager()

    def _get_llm(self):
        """Get a dynamically selected LLM"""
        try:
            config = get_dynamic_llm_config()
            return LLM(
                model=config["model"],
                api_key=config["api_key"],
                max_tokens=config["max_tokens"],
                temperature=config["temperature"]
            )
        except Exception as e:
            print(f"⚠️  Error getting LLM config: {e}")
            # Fallback to default
            return LLM(
                model=os.getenv("MODEL", "groq/llama-3.1-8b-instant"),
                api_key=os.getenv("GROQ_API_KEY"),
                max_tokens=4000,
                temperature=0.1
            )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[SearchTool(), NewsSearchTool()],
            llm=self._get_llm(),
            verbose=True,
            max_retry_limit=3,  # Retry with different LLMs
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            llm=self._get_llm(),
            verbose=True,
            max_retry_limit=3,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Enhanced Firstcrew with multi-LLM support"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            max_retry_limit=3,  # Retry failed tasks with different LLMs
        )