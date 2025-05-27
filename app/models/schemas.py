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


class CISFormPDFData(BaseModel):
    title: str = "Cis 2024 Ts 54521"
    fontSize: int = 10
    textColor: str = "#333333"
    data: Dict[str, str] = {
        "LicenseeNameforSellersandLandlords": "",
        "BrokerageNameforSellersandLandlords": "",
        "LicenseeNameBuyersandTenants": "",
        "BrokerageNameforBuyersandTenants": ""
    }
    documentType: Literal["cis_form"] = "cis_form"

class ComingSoonListingFormPDFData(BaseModel):
    title: str = "COMING SOON LISTING FORM"
    fontSize: int = 10
    textColor: str = "#333333"
    data: Dict[str, str] = {
        "sellersName1": "",
        "sellersName2": "",
        "sellersName3": "",
        "firstShownDate": "",
        "sellersSignatureDate1": "",
        "sellersSignatureDate2": "",
        "sellersSignatureDate3": ""
    }
    documentType: Literal["coming_soon_listing"] = "coming_soon_listing"

class MLSPropertyChangeFormPDFData(BaseModel):
    title: str = "Multiple Listing System Property Change Form 8 24"
    fontSize: int = 10
    textColor: str = "#333333"
    data: Dict[str, str] = {
        "propertyType": "",
        "ml#": "",
        "changeDate": "",
        "streetName": "",
        "officePhone": "",
        "agentPhone": "",
        "newListPriceperSqFt": "",
        "newExpirationDate": "",
        "fieldName1": "",
        "change1": "",
        "fieldName2": "",
        "change2": "",
        "fieldName3": "",
        "change3": "",
        "fieldName4": "",
        "change4": "",
        "additionalInformation": "",
        "TownName": "",
        "AgentName": "",
        "AgentID#": "",
        "OfficeID#": "",
        "OfficeName": "",
        "Street#": "",
        "BrokerName": "",
        "OwnerorLandlordName": ""
    }
    documentType: Literal["mls_change_form"] = "mls_change_form"

class InformedConsentFormPDFData(BaseModel):
    title: str = "Standard Form Of Informed Consent To Designated Agency Seller"
    fontSize: int = 10
    textColor: str = "#333333"
    data: Dict[str, str] = {
        "designatingBrokerName": "",
        "propertyAddress": "",
        "BrokerageFirmName": "",
        "LicenseeName": ""
    }
    documentType: Literal["informed_consent"] = "informed_consent"

class DualAgencyConsentFormPDFData(BaseModel):
    title: str = "Informed Consent To Dual Agency Seller"
    fontSize: int = 10
    textColor: str = "#333333"
    data: Dict[str, str] = {
        "propertyAddress": "",
        "LicenseeName": "",
        "NameofFirm": "",
        "BrokerageCityStateandZip": "",
        "BrokerageAddress": "",
        "BrokerageName": ""
    }
    documentType: Literal["dual_agency_consent"] = "dual_agency_consent"

# Use RootModel instead of __root__ field
class PDFData(RootModel[Union[SellerDisclosurePDFData, LeadBasedPaintDisclosurePDFData, CISFormPDFData, 
                              ComingSoonListingFormPDFData, MLSPropertyChangeFormPDFData, InformedConsentFormPDFData,
                              DualAgencyConsentFormPDFData]]):
    pass