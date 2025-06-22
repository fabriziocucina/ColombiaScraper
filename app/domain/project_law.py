from dataclasses import dataclass
from datetime import date
from typing import Optional, List
from enum import Enum

@dataclass
class Law:
    id: Optional[str]             
    country: str
    title: str
    objecto_projecto: str
    filing_date: date
    status: str
    pdf_links: List[str]
    sector: Optional[str] = None

class Country(Enum):
    COLOMBIA = "Colombia"

