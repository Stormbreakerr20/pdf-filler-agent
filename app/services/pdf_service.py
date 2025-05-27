import os
import uuid
from python_anvil.api import Anvil
from app.core.config import Config
from typing import Dict, Any


class PDFService:
    def __init__(self):
        self.anvil = Anvil(api_key=Config.ANVIL_API_KEY)
        self.default_template_eid = Config.PDF_TEMPLATE_EID
        self.seller_disclosure_template_eid = Config.SELLER_DISCLOSURE_TEMPLATE_EID
        self.lead_paint_disclosure_template_eid = Config.LEAD_PAINT_DISCLOSURE_TEMPLATE_EID
        self.cis_form_template_eid = Config.CIS_FORM_TEMPLATE_EID
        self.coming_soon_listing_template_eid = Config.COMING_SOON_LISTING_TEMPLATE_EID
        self.mls_change_form_template_eid = Config.MLS_CHANGE_FORM_TEMPLATE_EID
        self.informed_consent_template_eid = Config.INFORMED_CONSENT_TEMPLATE_EID
        self.dual_agency_consent_template_eid = Config.DUAL_AGENCY_CONSENT_TEMPLATE_EID
        self.output_dir = Config.BASE_OUTPUT_DIR
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def fill_pdf(self, pdf_data: Dict[str, Any], filename=None) -> str:
        """
        Fill PDF with the provided data and return the file path
        """
        # Generate unique filename
        if not filename:
            filename = f"out.pdf"
        file_path = os.path.join(self.output_dir, filename)
        
        # Determine which template to use based on document type
        template_eid = self.default_template_eid
        if pdf_data.get("documentType") == "seller_disclosure":
            template_eid = self.seller_disclosure_template_eid
        elif pdf_data.get("documentType") == "lead_based_paint_disclosure":
            template_eid = self.lead_paint_disclosure_template_eid
        elif pdf_data.get("documentType") == "cis_form":
            template_eid = self.cis_form_template_eid
        elif pdf_data.get("documentType") == "coming_soon_listing":
            template_eid = self.coming_soon_listing_template_eid
        elif pdf_data.get("documentType") == "mls_change_form":
            template_eid = self.mls_change_form_template_eid
        elif pdf_data.get("documentType") == "informed_consent":
            template_eid = self.informed_consent_template_eid
        elif pdf_data.get("documentType") == "dual_agency_consent":
            template_eid = self.dual_agency_consent_template_eid
        
        # Make PDF fill request
        response = self.anvil.fill_pdf(template_eid, pdf_data)
        
        # Save filled PDF
        with open(file_path, "wb") as f:
            f.write(response)
        
        return file_path