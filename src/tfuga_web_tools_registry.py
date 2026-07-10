"""TFUGAG Web Tools Registry.

Registry of approved web-accessible data sources and connectors.
This layer defines capabilities, rate limits, trust levels and review gates.
"""
from dataclasses import dataclass
from enum import Enum

class TrustLevel(str, Enum):
    HIGH='high'
    MEDIUM='medium'
    LOW='low'

@dataclass(frozen=True)
class WebTool:
    name:str
    purpose:str
    trust:TrustLevel
    requires_review:bool

APPROVED_WEB_TOOLS=[
    WebTool('arxiv','scientific papers ingestion',TrustLevel.HIGH,False),
    WebTool('crossref','citation metadata',TrustLevel.HIGH,False),
    WebTool('semantic_scholar','research graph',TrustLevel.HIGH,False),
    WebTool('github','repository intelligence',TrustLevel.HIGH,False),
    WebTool('patent_sources','patent discovery',TrustLevel.MEDIUM,True),
    WebTool('financial_feeds','market observation',TrustLevel.MEDIUM,True),
]

def list_tools():
    return APPROVED_WEB_TOOLS
