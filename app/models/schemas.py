from pydantic import BaseModel, Field, RootModel
from typing import List, Optional, Dict, Any, Union, Literal


class Message(BaseModel):
    role: str = "user"
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    user_id: Optional[str] = None
    document_type: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    pdf_url: Optional[str] = None
    user_id: str
    pdf_generated: bool = False

class SellerDisclosurePDFData(BaseModel):
    title: str = "Seller Property Condition Disclosure Statement 2 24 1"
    fontSize: int = 10
    textColor: str = "#333333"
    data: Dict[str, str] = {
        "ageOfHouse": "",
        "sellerOccupancyPeriod": "",
        "yearSellerBoughtProperty": "",
        "ageOfRoof": "",
        "cracksLocationInBasementFloorOrFoundationWalls": "",
        "termitesPestsCompanyInfo": "",
        "roofLeakExplanationIfAny": "",
        "WaterOrDampnessProblemInfo_location_nature_date_InBasementOrCrawlSpace": "",
        "explanationOfPestControlInspectionOrTreatements": ""
    }
    documentType: Literal["seller_disclosure"] = "seller_disclosure"


class LeadBasedPaintDisclosurePDFData(BaseModel):
    title: str = "Lead Based Paint Disclosure Addendum Leases"
    fontSize: int = 10
    textColor: str = "#333333"
    data: Dict[str, str] = {
        "lessorsDisclosureOfLeadBasedPaintHazards": "",
        "recordsAndReportsAvailability": "",
        "propertyAddress": "",
        "explanationOfKnownLeadBasedPaintHazards": "",
        "listOfDocumentsPertainingToLeadBasedHazards": ""
    }
    documentType: Literal["lead_based_paint_disclosure"] = "lead_based_paint_disclosure"


# Use RootModel instead of __root__ field
class PDFData(RootModel[Union[SellerDisclosurePDFData, LeadBasedPaintDisclosurePDFData]]):
    pass