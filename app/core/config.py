import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv("API_KEY", "your_default_api_key")
    PDF_TEMPLATE_EID = os.getenv("PDF_TEMPLATE_EID", "your_default_pdf_template_eid")
    SELLER_DISCLOSURE_TEMPLATE_EID = os.getenv("SELLER_DISCLOSURE_TEMPLATE_EID", "Ijgr02iZ8UoPpAKA4GkA")
    LEAD_PAINT_DISCLOSURE_TEMPLATE_EID = os.getenv("LEAD_PAINT_DISCLOSURE_TEMPLATE_EID", "your_lead_paint_template_eid")
    CIS_FORM_TEMPLATE_EID = os.getenv("CIS_FORM_TEMPLATE_EID", "your_cis_form_template_eid")
    COMING_SOON_LISTING_TEMPLATE_EID = os.getenv("COMING_SOON_LISTING_TEMPLATE_EID", "your_coming_soon_listing_template_eid")
    MLS_CHANGE_FORM_TEMPLATE_EID = os.getenv("MLS_CHANGE_FORM_TEMPLATE_EID", "your_mls_change_form_template_eid")
    INFORMED_CONSENT_TEMPLATE_EID = os.getenv("INFORMED_CONSENT_TEMPLATE_EID", "your_informed_consent_template_eid")
    DUAL_AGENCY_CONSENT_TEMPLATE_EID = os.getenv("DUAL_AGENCY_CONSENT_TEMPLATE_EID", "your_dual_agency_consent_template_eid")
    FILE_OUTPUT = os.getenv("FILE_OUTPUT", "fill-output.pdf")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your_groq_api_key")
    ANVIL_API_KEY = os.getenv("ANVIL_API_KEY", "your_anvil_api_key")
    MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
    BASE_OUTPUT_DIR = os.getenv("BASE_OUTPUT_DIR", "./output")