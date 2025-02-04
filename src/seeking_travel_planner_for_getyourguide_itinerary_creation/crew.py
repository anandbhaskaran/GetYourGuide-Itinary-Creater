from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool, WebsiteSearchTool, SerpApiGoogleSearchTool, SerperDevTool
from pydantic import BaseModel, Field
from typing import List, Optional


class Activity(BaseModel):
    name: str = Field(..., description="Name of the activity")
    location: str = Field(..., description="Location of the activity")
    description: str = Field(..., description="Description of the activity")
    date: str = Field(..., description="Date of the activity")
    booking_link: str = Field(..., description="GetYourGuide booking link")
    why_its_suitable: str = Field(..., description="Why it's suitable for the traveler")
    reviews: Optional[List[str]] = Field(..., description="List of reviews")
    rating: Optional[float] = Field(..., description="Rating of the activity")


class DayPlan(BaseModel):
    date: str = Field(..., description="Date of the day")
    activities: List[Activity] = Field(..., description="List of activities")
    restaurants: List[str] = Field(..., description="List of restaurants")
    flight: Optional[str] = Field(None, description="Flight information")


class Itinerary(BaseModel):
    name: str = Field(..., description="Name of the itinerary, something funny")
    day_plans: List[DayPlan] = Field(..., description="List of day plans")
    hotel: str = Field(..., description="Hotel information")


@CrewBase
class SeekingTravelPlannerForGetyourguideItineraryCreationCrew():
    """SeekingTravelPlannerForGetyourguideItineraryCreation crew"""

    @agent
    def TravelPlannerAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['TravelPlannerAgent'],
            tools=[WebsiteSearchTool(), ScrapeWebsiteTool()],
            # tools=[WebsiteSearchTool(), SerpApiGoogleSearchTool()],
        )

    @task
    def FindActivities(self) -> Task:
        return Task(
            config=self.tasks_config['FindActivities'],
            tools=[WebsiteSearchTool(), ScrapeWebsiteTool(),
                   SerperDevTool(n_results=10,  save_file=True, search_type="search")],
            # tools=[WebsiteSearchTool(), SerpApiGoogleSearchTool()],
        )

    @task
    def ScrapeYourGuide(self) -> Task:
        return Task(
            config=self.tasks_config['ScrapeYourGuide'],
            tools=[WebsiteSearchTool(), ScrapeWebsiteTool()],
        )

    @task
    def FilterActivities(self) -> Task:
        return Task(
            config=self.tasks_config['FilterActivities'],
            tools=[],
        )

    @task
    def CreateItinerary(self) -> Task:
        return Task(
            config=self.tasks_config['CreateItinerary'],
            tools=[],
            output_json=Itinerary
        )

    @task
    def CreateMarkdownFile(self) -> Task:
        return Task(
            config=self.tasks_config['CreateMarkdownFile'],
            tools=[],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SeekingTravelPlannerForGetyourguideItineraryCreation crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
