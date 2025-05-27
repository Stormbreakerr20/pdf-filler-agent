import json
import re
from groq import Groq
from app.core.config import Config
from app.models.schemas import Message
from typing import List, Tuple, Dict, Any, Optional

# Update the get_system_message function:

def get_system_message(document_type="default"):
    if document_type == "seller_disclosure":
        return """You are a helpful assistant that collects information for filling out Seller Property Condition Disclosure Statements.
        Extract the following details in a conversational way:
        - Age of house
        - Seller occupancy period
        - Year seller bought property
        - Age of roof
        - Information about cracks in basement, floor, or foundation walls
        - Information about termites or pests, including company info
        - Information about roof leaks, if any
        - Information about water or dampness problems in basement or crawl space, including location, nature, and date
        - Explanations of pest control inspections or treatments
        
        Extract information gradually and naturally during the conversation. Be friendly and conversational.
        
        When you identify information, include it in a structured JSON format at the end of your response.
        Format the extracted information as:
        
        EXTRACT_JSON: {
          "data": {
            "ageOfHouse": "...",
            "sellerOccupancyPeriod": "...",
            "yearSellerBoughtProperty": "...",
            "ageOfRoof": "...",
            "cracksLocationInBasementFloorOrFoundationWalls": "...",
            "termitesPestsCompanyInfo": "...",
            "roofLeakExplanationIfAny": "...",
            "WaterOrDampnessProblemInfo_location_nature_date_InBasementOrCrawlSpace": "...",
            "explanationOfPestControlInspectionOrTreatements": "..."
          }
        }
        
        Only include fields you extracted from the current message. If no information was extracted, 
        don't include the EXTRACT_JSON section at all.
        
        IMPORTANT: The JSON extraction section should not be visible to users.
        """
    elif document_type == "lead_based_paint_disclosure":
        return """You are a helpful assistant that collects information for filling out Lead Based Paint Disclosure Addendum Leases.
        Extract the following details in a conversational way:
        - Property address
        - Lessor's disclosure of lead-based paint hazards (Known lead-based paint hazards present or None known)
        - Records and reports availability (Available or Not available)
        - Explanation of known lead-based paint hazards, if any
        - List of documents pertaining to lead-based hazards, if any
        
        Extract information gradually and naturally during the conversation. Be friendly and conversational.
        
        When you identify information, include it in a structured JSON format at the end of your response.
        Format the extracted information as:
        
        EXTRACT_JSON: {
          "data": {
            "propertyAddress": "...",
            "lessorsDisclosureOfLeadBasedPaintHazards": "...",
            "recordsAndReportsAvailability": "...",
            "explanationOfKnownLeadBasedPaintHazards": "...",
            "listOfDocumentsPertainingToLeadBasedHazards": "..."
          }
        }
        
        Only include fields you extracted from the current message. If no information was extracted, 
        don't include the EXTRACT_JSON section at all.
        
        IMPORTANT: The JSON extraction section should not be visible to users.
        """
    elif document_type == "cis_form":
        return """You are a helpful assistant that collects information for filling out CIS (Consumer Information Statement) Forms.
        Extract the following details in a conversational way:
        - Licensee Name for Sellers and Landlords
        - Brokerage Name for Sellers and Landlords 
        - Licensee Name for Buyers and Tenants
        - Brokerage Name for Buyers and Tenants
        
        Extract information gradually and naturally during the conversation. Be friendly and conversational.
        
        When you identify information, include it in a structured JSON format at the end of your response.
        Format the extracted information as:
        
        EXTRACT_JSON: {
          "data": {
            "LicenseeNameforSellersandLandlords": "...",
            "BrokerageNameforSellersandLandlords": "...",
            "LicenseeNameBuyersandTenants": "...",
            "BrokerageNameforBuyersandTenants": "..."
          }
        }
        
        Only include fields you extracted from the current message. If no information was extracted, 
        don't include the EXTRACT_JSON section at all.
        
        IMPORTANT: The JSON extraction section should not be visible to users.
        """
    elif document_type == "coming_soon_listing":
        return """You are a helpful assistant that collects information for filling out Coming Soon Listing Forms.
        Extract the following details in a conversational way:
        - Seller's Name (up to 3 different sellers can be added)
        - First Shown Date
        - Seller's Signature Date (for each seller)
        
        Extract information gradually and naturally during the conversation. Be friendly and conversational.
        
        When you identify information, include it in a structured JSON format at the end of your response.
        Format the extracted information as:
        
        EXTRACT_JSON: {
          "data": {
            "sellersName1": "...",
            "sellersName2": "...",
            "sellersName3": "...",
            "firstShownDate": "...",
            "sellersSignatureDate1": "...",
            "sellersSignatureDate2": "...",
            "sellersSignatureDate3": "..."
          }
        }
        
        Only include fields you extracted from the current message. If no information was extracted, 
        don't include the EXTRACT_JSON section at all.
        
        IMPORTANT: The JSON extraction section should not be visible to users.
        """
    elif document_type == "mls_change_form":
        return """You are a helpful assistant that collects information for filling out Multiple Listing System (MLS) Property Change Forms.
        Extract the following details in a conversational way:
        
        - Property Type (must be one of: "Property Type: RES", "Property Type: MUL", "Property Type: LND", 
          "Property Type: COM", "Property Type: BUS", "Property Type: RNT")
        - MLS# (ml#)
        - Change Date
        - Street Name and Number (Street#)
        - Town Name
        - Agent Information (Name, ID#, Phone)
        - Office Information (Name, ID#, Phone)
        - Broker Name
        - Owner or Landlord Name
        - Any field changes (fieldName1-4 and change1-4)
        - New List Price per Square Foot (if applicable)
        - New Expiration Date (if applicable)
        - Additional Information (if provided)

        Extract information gradually and naturally during the conversation. Be friendly and conversational.
        
        When you identify information, include it in a structured JSON format at the end of your response.
        Format the extracted information as:
        
        EXTRACT_JSON: {
          "data": {
            "propertyType": "...",
            "ml#": "...",
            "changeDate": "...",
            "streetName": "...",
            "officePhone": "...",
            "agentPhone": "...",
            "newListPriceperSqFt": "...",
            "newExpirationDate": "...",
            "fieldName1": "...",
            "change1": "...",
            "fieldName2": "...",
            "change2": "...",
            "fieldName3": "...",
            "change3": "...",
            "fieldName4": "...",
            "change4": "...",
            "additionalInformation": "...",
            "TownName": "...",
            "AgentName": "...",
            "AgentID#": "...",
            "OfficeID#": "...",
            "OfficeName": "...",
            "Street#": "...",
            "BrokerName": "...",
            "OwnerorLandlordName": "..."
          }
        }
        
        Only include fields you extracted from the current message. If no information was extracted, 
        don't include the EXTRACT_JSON section at all.
        
        IMPORTANT: The JSON extraction section should not be visible to users.
        """
    elif document_type == "informed_consent":
        return """You are a helpful assistant that collects information for filling out the Standard Form Of Informed Consent To Designated Agency Seller.
        Extract the following details in a conversational way:
        
        - Designating Broker Name
        - Property Address
        - Brokerage Firm Name
        - Licensee Name
        
        Extract information gradually and naturally during the conversation. Be friendly and conversational.
        
        When you identify information, include it in a structured JSON format at the end of your response.
        Format the extracted information as:
        
        EXTRACT_JSON: {
          "data": {
            "designatingBrokerName": "...",
            "propertyAddress": "...",
            "BrokerageFirmName": "...",
            "LicenseeName": "..."
          }
        }
        
        Only include fields you extracted from the current message. If no information was extracted, 
        don't include the EXTRACT_JSON section at all.
        
        IMPORTANT: The JSON extraction section should not be visible to users.
        """
    elif document_type == "dual_agency_consent":
        return """You are a helpful assistant that collects information for filling out the Informed Consent To Dual Agency Seller form.
        Extract the following details in a conversational way:
        
        - Property Address
        - Licensee Name
        - Name of Firm
        - Brokerage Name
        - Brokerage Address
        - Brokerage City, State, and Zip
        
        Extract information gradually and naturally during the conversation. Be friendly and conversational.
        
        When you identify information, include it in a structured JSON format at the end of your response.
        Format the extracted information as:
        
        EXTRACT_JSON: {
          "data": {
            "propertyAddress": "...",
            "LicenseeName": "...",
            "NameofFirm": "...",
            "BrokerageCityStateandZip": "...",
            "BrokerageAddress": "...",
            "BrokerageName": "..."
          }
        }
        
        Only include fields you extracted from the current message. If no information was extracted, 
        don't include the EXTRACT_JSON section at all.
        
        IMPORTANT: The JSON extraction section should not be visible to users.
        """
    return """You are a helpful assistant that collects information for filling out forms.
    Extract information gradually and naturally during the conversation. Be friendly and conversational.
    """

class ChatbotService:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.MODEL_NAME

    # Update the process_chat method to get the system message based on document type:

    async def process_chat(self, messages: List[Message], document_type: str = "default") -> Tuple[str, Optional[Dict[str, Any]]]:
        # Get the appropriate system message
        system_message = get_system_message(document_type)
        
        # Add system message if not present
        print(messages)
        chat_messages = [{"role": "system", "content": system_message}]
        
        # Add user messages
        for msg in messages:
            chat_messages.append({"role": msg.role, "content": msg.content})
        
        # Get completion from Groq
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=chat_messages,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
        )
        
        response_text = completion.choices[0].message.content
        
        # Extract JSON if present
        extracted_data = self._extract_json(response_text)
    
        # Clean response for user (remove the JSON extraction part)
        cleaned_response = re.sub(r'EXTRACT_JSON:.*', '', response_text, flags=re.DOTALL).strip()
        
        return cleaned_response, extracted_data
    
    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract JSON data from the response text."""
        match = re.search(r'EXTRACT_JSON:\s*({.*?)(?=\n\n|\Z)', text, re.DOTALL)
        if match:
            try:
                json_str = match.group(1)
                # Try to parse the JSON
                parsed_data = json.loads(json_str)
                return parsed_data
            except json.JSONDecodeError as e:
                
                # Try to fix common issues with JSON
                try:
                    # Count opening and closing braces to ensure they match
                    open_braces = json_str.count('{')
                    close_braces = json_str.count('}')
                    
                    # If we have more opening braces than closing, add the missing ones
                    if open_braces > close_braces:
                        json_str = json_str + ('}' * (open_braces - close_braces))
                        print("Fixed JSON by adding missing braces:", json_str)
                    
                    # Remove any potential comments
                    cleaned_json = re.sub(r'//.*?(\n|$)', '', json_str)
                    # Replace single quotes with double quotes
                    cleaned_json = cleaned_json.replace("'", '"')
                    # Make sure property names are quoted
                    cleaned_json = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', cleaned_json)
                    
                    print("Cleaned JSON string:", cleaned_json)
                    parsed_data = json.loads(cleaned_json)
                    print("Successfully parsed cleaned JSON:", parsed_data)
                    return parsed_data
                except Exception as fix_error:
                    print("Failed to fix JSON:", fix_error)
                    return None
                    
        
        # For non-matches or if all extraction attempts fail
        print("No valid JSON found")
        return None