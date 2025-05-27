from app.core.database import get_connection, release_connection
from app.models.schemas import Message
import json
import uuid
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class PGMemoryService:
    """PostgreSQL-based memory service with performance optimizations"""
    
    def get_or_create_session(self, user_id: Optional[str] = None, document_type: str = "default") -> str:
        """Get or create a user session"""
        if not user_id:
            user_id = str(uuid.uuid4())
            
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Use prepared statement with parameters
            cursor.execute(
                "SELECT id FROM user_sessions WHERE user_id = %s AND document_type = %s",
                (user_id, document_type)
            )
            result = cursor.fetchone()
            
            if not result:
                # Create session and initialize data in a single transaction
                cursor.execute(
                    "INSERT INTO user_sessions (user_id, document_type) VALUES (%s, %s) RETURNING id",
                    (user_id, document_type)
                )
                session_id = cursor.fetchone()[0]
                
                # Initialize with appropriate template
                initial_data = self._get_initial_data(document_type)
                
                cursor.execute(
                    "INSERT INTO form_data (session_id, data) VALUES (%s, %s)",
                    (session_id, json.dumps(initial_data))
                )
                conn.commit()
            
            return user_id
            
        except Exception as e:
            logger.error(f"Error in get_or_create_session: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                release_connection(conn)
                
        return user_id
    
    def add_message(self, user_id: str, message: Message) -> None:
        """Save a message to the database"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # More efficient - get session ID with document_type for cache locality
            cursor.execute(
                """
                SELECT id FROM user_sessions 
                WHERE user_id = %s 
                ORDER BY created_at DESC LIMIT 1
                """,
                (user_id,)
            )
            result = cursor.fetchone()
            
            if result:
                session_id = result[0]
                cursor.execute(
                    "INSERT INTO messages (session_id, role, content) VALUES (%s, %s, %s)",
                    (session_id, message.role, message.content)
                )
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error adding message: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                release_connection(conn)
    
    def get_messages(self, user_id: str) -> List[Message]:
        """Get all messages for a user"""
        messages = []
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # More efficient query - join to get messages directly
            cursor.execute(
                """
                SELECT m.role, m.content 
                FROM messages m
                JOIN user_sessions s ON m.session_id = s.id
                WHERE s.user_id = %s
                ORDER BY m.timestamp
                """,
                (user_id,)
            )
            
            for row in cursor.fetchall():
                messages.append(Message(role=row[0], content=row[1]))
                
        except Exception as e:
            logger.error(f"Error getting messages: {e}")
        finally:
            if conn:
                release_connection(conn)
                
        return messages
    
    def update_collected_data(self, user_id: str, data: Dict[str, Any]) -> None:
        """Update form data"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Get session ID
            cursor.execute(
                "SELECT id FROM user_sessions WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
                (user_id,)
            )
            result = cursor.fetchone()
            
            if result:
                session_id = result[0]
                
                # Get current data
                cursor.execute(
                    "SELECT data FROM form_data WHERE session_id = %s",
                    (session_id,)
                )
                current_data = cursor.fetchone()
                
                if current_data:
                    # Merge data
                    current_dict = current_data[0]
                    self._update_nested_dict(current_dict, data)
                    
                    # Update in database
                    cursor.execute(
                        "UPDATE form_data SET data = %s WHERE session_id = %s",
                        (json.dumps(current_dict), session_id)
                    )
                    conn.commit()
                
        except Exception as e:
            logger.error(f"Error updating data: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                release_connection(conn)
    
    def get_collected_data(self, user_id: str) -> Dict[str, Any]:
        """Get collected form data"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Get session ID
            cursor.execute(
                "SELECT id FROM user_sessions WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
                (user_id,)
            )
            result = cursor.fetchone()
            
            if result:
                session_id = result[0]
                
                # Get form data
                cursor.execute(
                    "SELECT data FROM form_data WHERE session_id = %s",
                    (session_id,)
                )
                data = cursor.fetchone()
                
                if data:
                    return data[0]
            
            return {}
            
        except Exception as e:
            logger.error(f"Error getting collected data: {e}")
            return {}
        finally:
            if conn:
                release_connection(conn)
    
    def clear_session(self, user_id: str) -> None:
        """Delete a user's session"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Delete session (cascades to messages and form data)
            cursor.execute(
                "DELETE FROM user_sessions WHERE user_id = %s",
                (user_id,)
            )
            conn.commit()
            
        except Exception as e:
            logger.error(f"Error clearing session: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                release_connection(conn)
    
    def is_data_complete(self, user_id: str) -> bool:
        """Check if enough data has been collected to generate PDF"""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Get session and document type
            cursor.execute(
                "SELECT id, document_type FROM user_sessions WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
                (user_id,)
            )
            result = cursor.fetchone()
            
            if not result:
                return False
                
            session_id, document_type = result
            
            # Get form data
            cursor.execute(
                "SELECT data FROM form_data WHERE session_id = %s",
                (session_id,)
            )
            data_row = cursor.fetchone()
            
            if not data_row:
                return False
                
            data = data_row[0]
            
            # Simple check for required fields
            if document_type == "seller_disclosure":
                return "data" in data and "ageOfHouse" in data["data"] and data["data"]["ageOfHouse"]
            elif document_type == "lead_based_paint_disclosure":
                return "data" in data and "propertyAddress" in data["data"] and data["data"]["propertyAddress"]
            elif document_type == "cis_form":
                return ("data" in data and 
                       "LicenseeNameforSellersandLandlords" in data["data"] and 
                       data["data"]["LicenseeNameforSellersandLandlords"])
            elif document_type == "coming_soon_listing":
                return ("data" in data and 
                       "sellersName1" in data["data"] and 
                       "firstShownDate" in data["data"] and
                       data["data"]["sellersName1"] and
                       data["data"]["firstShownDate"])
            elif document_type == "mls_change_form":
                return ("data" in data and 
                       "propertyType" in data["data"] and
                       "ml#" in data["data"] and
                       "changeDate" in data["data"] and
                       "AgentName" in data["data"] and
                       data["data"]["propertyType"] and
                       data["data"]["ml#"] and
                       data["data"]["changeDate"] and
                       data["data"]["AgentName"])
            elif document_type == "informed_consent":
                return ("data" in data and 
                       "designatingBrokerName" in data["data"] and
                       "propertyAddress" in data["data"] and
                       "BrokerageFirmName" in data["data"] and
                       "LicenseeName" in data["data"] and
                       data["data"]["designatingBrokerName"] and
                       data["data"]["propertyAddress"] and
                       data["data"]["BrokerageFirmName"] and
                       data["data"]["LicenseeName"])
            elif document_type == "dual_agency_consent":
                return ("data" in data and 
                       "propertyAddress" in data["data"] and
                       "LicenseeName" in data["data"] and
                       "BrokerageName" in data["data"] and
                       data["data"]["propertyAddress"] and
                       data["data"]["LicenseeName"] and
                       data["data"]["BrokerageName"])
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking if data complete: {e}")
            return False
        finally:
            if conn:
                release_connection(conn)
    
    def set_document_type(self, user_id: str, document_type: str) -> None:
        """Set document type for a session"""
        self.get_or_create_session(user_id, document_type)
    
    # Helper methods
    def _get_initial_data(self, document_type: str) -> Dict[str, Any]:
        """Get initial data structure based on document type"""
        if document_type == "seller_disclosure":
            return {
                "documentType": "seller_disclosure",
                "data": {
                    "ageOfHouse": "",
                    "sellerOccupancyPeriod": "",
                    "yearSellerBoughtProperty": ""
                }
            }
        elif document_type == "lead_based_paint_disclosure":
            return {
                "documentType": "lead_based_paint_disclosure",
                "data": {
                    "propertyAddress": "",
                    "lessorsDisclosureOfLeadBasedPaintHazards": ""
                }
            }
        elif document_type == "cis_form":
            return {
                "documentType": "cis_form",
                "data": {
                    "LicenseeNameforSellersandLandlords": "",
                    "BrokerageNameforSellersandLandlords": "",
                    "LicenseeNameBuyersandTenants": "",
                    "BrokerageNameforBuyersandTenants": ""
                }
            }
        elif document_type == "coming_soon_listing":
            return {
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
            return {
                "documentType": "mls_change_form",
                "data": {
                    "propertyType": "",
                    "ml#": "",
                    "changeDate": "",
                    "streetName": "",
                    "AgentName": "",
                    "TownName": "",
                    "OwnerorLandlordName": ""
                }
            }
        elif document_type == "informed_consent":
            return {
                "documentType": "informed_consent",
                "data": {
                    "designatingBrokerName": "",
                    "propertyAddress": "",
                    "BrokerageFirmName": "",
                    "LicenseeName": ""
                }
            }
        elif document_type == "dual_agency_consent":
            return {
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
        else:
            return {
                "documentType": document_type,
                "data": {}
            }
    
    def _update_nested_dict(self, target: Dict, source: Dict) -> None:
        """Merge source dict into target dict"""
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._update_nested_dict(target[key], value)
            else:
                target[key] = value