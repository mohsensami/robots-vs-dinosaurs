from typing import Optional, List, Dict
from pydantic import BaseModel


class GamePayload(BaseModel):

    """ The data model for starting games """

    grid_dim: int = 10
    robots_count: Optional[int] = None
    robots: List[Dict] = []
    dinosaurs_count: Optional[int] = None
    dinosaurs: Optional[List[tuple]] = []

