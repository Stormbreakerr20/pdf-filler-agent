from typing import Dict, List, Any, Optional, Tuple
import uuid
from app.models.schemas import Message


class MemoryService:
    def __init__(self):
        # Change sessions to be organized by user_id and document_type
        self._sessions: Dict[Tuple[str, str], List[Message]] = {}
        self._collected_data: Dict[str, Dict[str, Any]] = {}
        self._document_types: Dict[str, str] = {}
        
    def get_or_create_session(self, user_id: Optional[str] = None, document_type: str = "default") -> str:
        """Get an existing session or create a new one"""
        if not user_id:
            user_id = str(uuid.uuid4())
        
        # Create a session key using both user_id and document_type
        session_key = (user_id, document_type)
        
        if session_key not in self._sessions:
            self._sessions[session_key] = []
            self._document_types[user_id] = document_type
            
            if document_type == "seller_disclosure":
                self._collected_data[user_id] = {
                    "title": "Seller Property Condition Disclosure Statement 2 24 1",
                    "fontSize": 10,
                    "textColor": "#333333",
                    "documentType": "seller_disclosure",
                    "data": {
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
                }
            elif document_type == "lead_based_paint_disclosure":
                self._collected_data[user_id] = {
                    "title": "Lead Based Paint Disclosure Addendum Leases",
                    "fontSize": 10,
                    "textColor": "#333333",
                    "documentType": "lead_based_paint_disclosure",
                    "data": {
                        "lessorsDisclosureOfLeadBasedPaintHazards": "",
                        "recordsAndReportsAvailability": "",
                        "propertyAddress": "",
                        "explanationOfKnownLeadBasedPaintHazards": "",
                        "listOfDocumentsPertainingToLeadBasedHazards": ""
                    }
                }
            elif document_type == "cis_form":
                self._collected_data[user_id] = {
                    "title": "Cis 2024 Ts 54521",
                    "fontSize": 10,
                    "textColor": "#333333",
                    "documentType": "cis_form",
                    "data": {
                        "LicenseeNameforSellersandLandlords": "",
                        "BrokerageNameforSellersandLandlords": "",
                        "LicenseeNameBuyersandTenants": "",
                        "BrokerageNameforBuyersandTenants": ""
                    }
                }
            elif document_type == "coming_soon_listing":
                self._collected_data[user_id] = {
                    "title": "COMING SOON LISTING FORM",
                    "fontSize": 10,
                    "textColor": "#333333",
                    "documentType": "coming_soon_listing",
                    "data": {
                        "sellersName1": "",
                        "sellersName2": "",
                        "sellersName3": "",
                        "firstShownDate": "",
                        "sellersSignatureDate1": "",
                        "sellersSignatureDate2": "",
                        "sellersSignatureDate3": ""
                    }
                }
            elif document_type == "mls_change_form":
                self._collected_data[user_id] = {
                    "title": "Multiple Listing System Property Change Form 8 24",
                    "fontSize": 10,
                    "textColor": "#333333",
                    "documentType": "mls_change_form",
                    "data": {
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
                }
            elif document_type == "informed_consent":
                self._collected_data[user_id] = {
                    "title": "Standard Form Of Informed Consent To Designated Agency Seller",
                    "fontSize": 10,
                    "textColor": "#333333",
                    "documentType": "informed_consent",
                    "data": {
                        "designatingBrokerName": "",
                        "propertyAddress": "",
                        "BrokerageFirmName": "",
                        "LicenseeName": ""
                    }
                }
            elif document_type == "dual_agency_consent":
                self._collected_data[user_id] = {
                    "title": "Informed Consent To Dual Agency Seller",
                    "fontSize": 10,
                    "textColor": "#333333",
                    "documentType": "dual_agency_consent",
                    "data": {
                        "propertyAddress": "",
                        "LicenseeName": "",
                        "NameofFirm": "",
                        "BrokerageCityStateandZip": "",
                        "BrokerageAddress": "",
                        "BrokerageName": ""
                    }
                }
            
        return user_id
    
    def set_document_type(self, user_id: str, document_type: str) -> None:
        """Set the document type for a session"""
        self._document_types[user_id] = document_type
        
        # Initialize the appropriate data structure if changing document type
        if document_type == "seller_disclosure" and (user_id not in self._collected_data or 
                                                    self._collected_data[user_id].get("documentType") != "seller_disclosure"):
            self._collected_data[user_id] = {
                "title": "Seller Property Condition Disclosure Statement 2 24 1",
                "fontSize": 10,
                "textColor": "#333333",
                "documentType": "seller_disclosure",
                "data": {
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
            }
        elif document_type == "lead_based_paint_disclosure" and (user_id not in self._collected_data or 
                                                               self._collected_data[user_id].get("documentType") != "lead_based_paint_disclosure"):
            self._collected_data[user_id] = {
                "title": "Lead Based Paint Disclosure Addendum Leases",
                "fontSize": 10,
                "textColor": "#333333",
                "documentType": "lead_based_paint_disclosure",
                "data": {
                    "lessorsDisclosureOfLeadBasedPaintHazards": "",
                    "recordsAndReportsAvailability": "",
                    "propertyAddress": "",
                    "explanationOfKnownLeadBasedPaintHazards": "",
                    "listOfDocumentsPertainingToLeadBasedHazards": ""
                }
            }
        elif document_type == "cis_form" and (user_id not in self._collected_data or
                                            self._collected_data[user_id].get("documentType") != "cis_form"):
            self._collected_data[user_id] = {
                "title": "Cis 2024 Ts 54521",
                "fontSize": 10,
                "textColor": "#333333",
                "documentType": "cis_form",
                "data": {
                    "LicenseeNameforSellersandLandlords": "",
                    "BrokerageNameforSellersandLandlords": "",
                    "LicenseeNameBuyersandTenants": "",
                    "BrokerageNameforBuyersandTenants": ""
                }
            }
        elif document_type == "coming_soon_listing" and (user_id not in self._collected_data or
                                                     self._collected_data[user_id].get("documentType") != "coming_soon_listing"):
            self._collected_data[user_id] = {
                "title": "COMING SOON LISTING FORM",
                "fontSize": 10,
                "textColor": "#333333",
                "documentType": "coming_soon_listing",
                "data": {
                    "sellersName1": "",
                    "sellersName2": "",
                    "sellersName3": "",
                    "firstShownDate": "",
                    "sellersSignatureDate1": "",
                    "sellersSignatureDate2": "",
                    "sellersSignatureDate3": ""
                }
            }
        elif document_type == "mls_change_form" and (user_id not in self._collected_data or
                                                  self._collected_data[user_id].get("documentType") != "mls_change_form"):
            self._collected_data[user_id] = {
                "title": "Multiple Listing System Property Change Form 8 24",
                "fontSize": 10,
                "textColor": "#333333",
                "documentType": "mls_change_form",
                "data": {
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
            }
        elif document_type == "informed_consent" and (user_id not in self._collected_data or
                                                   self._collected_data[user_id].get("documentType") != "informed_consent"):
            self._collected_data[user_id] = {
                "title": "Standard Form Of Informed Consent To Designated Agency Seller",
                "fontSize": 10,
                "textColor": "#333333",
                "documentType": "informed_consent",
                "data": {
                    "designatingBrokerName": "",
                    "propertyAddress": "",
                    "BrokerageFirmName": "",
                    "LicenseeName": ""
                }
            }
        elif document_type == "dual_agency_consent" and (user_id not in self._collected_data or
                                                     self._collected_data[user_id].get("documentType") != "dual_agency_consent"):
            self._collected_data[user_id] = {
                "title": "Informed Consent To Dual Agency Seller",
                "fontSize": 10,
                "textColor": "#333333",
                "documentType": "dual_agency_consent",
                "data": {
                    "propertyAddress": "",
                    "LicenseeName": "",
                    "NameofFirm": "",
                    "BrokerageCityStateandZip": "",
                    "BrokerageAddress": "",
                    "BrokerageName": ""
                }
            }
    
    def add_message(self, user_id: str, message: Message) -> None:
        """Add a message to the session history"""
        # Get the current document type for this user
        document_type = self._document_types.get(user_id, "default")
        session_key = (user_id, document_type)
        
        if session_key not in self._sessions:
            self.get_or_create_session(user_id, document_type)
        
        self._sessions[session_key].append(message)
    
    def get_messages(self, user_id: str) -> List[Message]:
        """Get all messages for a session"""
        # Get the current document type for this user
        document_type = self._document_types.get(user_id, "default")
        session_key = (user_id, document_type)
        
        return self._sessions.get(session_key, [])
    
    def update_collected_data(self, user_id: str, data: Dict[str, Any]) -> None:
        """Update the collected data for a user"""
        if user_id not in self._collected_data:
            # Get the document type for this user
            document_type = self._document_types.get(user_id, "default")
            self.get_or_create_session(user_id, document_type)
        
        # Merge new data with existing data
        self._update_nested_dict(self._collected_data[user_id], data)
    
    def get_collected_data(self, user_id: str) -> Dict[str, Any]:
        """Get collected data for a user"""
        return self._collected_data.get(user_id, {})
    
    def clear_session(self, user_id: str) -> None:
        """Clear all sessions for a user"""
        # Remove all sessions associated with this user ID across all document types
        for key in list(self._sessions.keys()):
            session_user_id, _ = key
            if session_user_id == user_id:
                del self._sessions[key]
                
        if user_id in self._collected_data:
            del self._collected_data[user_id]
        if user_id in self._document_types:
            del self._document_types[user_id]
    
    def _update_nested_dict(self, target: Dict, source: Dict) -> None:
        """Update a nested dictionary with another one"""
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._update_nested_dict(target[key], value)
            else:
                target[key] = value
                
    def is_data_complete(self, user_id: str) -> bool:
        """Check if we have enough data to generate a PDF"""
        if user_id not in self._collected_data:
            return False
            
        data = self._collected_data[user_id]
        document_type = data.get("documentType", "default")
        
        if document_type == "seller_disclosure":
            # For seller disclosure, check if required fields are filled
            if "data" not in data:
                return False
                
            required_fields = [
                "ageOfHouse", 
                "sellerOccupancyPeriod", 
                "yearSellerBoughtProperty"
            ]
            
            for field in required_fields:
                if not data["data"].get(field):
                    return False
                    
            return True
        elif document_type == "lead_based_paint_disclosure":
            # For lead based paint disclosure, check if required fields are filled
            if "data" not in data:
                return False
                
            required_fields = [
                "propertyAddress", 
                "lessorsDisclosureOfLeadBasedPaintHazards"
            ]
            
            for field in required_fields:
                if not data["data"].get(field):
                    return False
                    
            return True
        elif document_type == "cis_form":
            # For CIS form, check if required fields are filled
            if "data" not in data:
                return False
                
            required_fields = [
                "LicenseeNameforSellersandLandlords",
                "BrokerageNameforSellersandLandlords"
            ]
            
            for field in required_fields:
                if not data["data"].get(field):
                    return False
                    
            return True
        elif document_type == "coming_soon_listing":
            # For coming soon listing, check if required fields are filled
            if "data" not in data:
                return False
                
            required_fields = [
                "sellersName1",
                "firstShownDate" 
            ]
            
            for field in required_fields:
                if not data["data"].get(field):
                    return False
                    
            return True
        elif document_type == "mls_change_form":
            # For MLS Change Form, check if required fields are filled
            if "data" not in data:
                return False
                
            required_fields = [
                "propertyType",
                "ml#",
                "changeDate",
                "AgentName"
            ]
            
            for field in required_fields:
                if not data["data"].get(field):
                    return False
                    
            return True
        elif document_type == "informed_consent":
            # For Informed Consent Form, check if required fields are filled
            if "data" not in data:
                return False
                
            required_fields = [
                "designatingBrokerName",
                "propertyAddress",
                "BrokerageFirmName",
                "LicenseeName"
            ]
            
            for field in required_fields:
                if not data["data"].get(field):
                    return False
                    
            return True
        elif document_type == "dual_agency_consent":
            # For Dual Agency Consent Form, check if required fields are filled
            if "data" not in data:
                return False
                
            required_fields = [
                "propertyAddress",
                "LicenseeName",
                "BrokerageName"
            ]
            
            for field in required_fields:
                if not data["data"].get(field):
                    return False
                    
            return True