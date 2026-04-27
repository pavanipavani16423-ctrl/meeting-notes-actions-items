from typing import List
from pydantic import BaseModel, Field


class ActionItem(BaseModel):
    task: str = Field(
        description="The task to be completed"
    )
    owner: str = Field(
        default="not_available",
        description="Person responsible for the task"
    )
    deadline: str = Field(
        default="not_available",
        description="Deadline or due date for the task"
    )
    priority: str = Field(
        default="Medium",
        description="Priority level: High, Medium, or Low"
    )


class ActionItemsOutput(BaseModel):
    actions: List[ActionItem] = Field(
        description="List of all action items extracted from meeting notes"
    )