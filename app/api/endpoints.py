from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from app.models.schemas import ChatRequest, ChatResponse, Message
from app.services.chatbot import ChatbotService
from app.services.pdf_service import PDFService
from app.services.pg_memory_service import PGMemoryService
import os
from typing import Optional

router = APIRouter()
chatbot_service = ChatbotService()
pdf_service = PDFService()
memory_service = PGMemoryService()  # Use PostgreSQL memory service instead

@router.post("/chat")
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    """
    Process a chat message, maintain conversation memory, and generate PDF when enough data is collected
    """
    try:
        # Get or create session with document type
        document_type = request.document_type or "default"
        user_id = memory_service.get_or_create_session(request.user_id, document_type)
        
        # Get the last user message only
        last_message = request.messages[-1] if request.messages else None
        if last_message and last_message.role == "user":
            # Add user message to memory
            memory_service.add_message(user_id, last_message)
            
            # Get all historic messages for context
            all_messages = memory_service.get_messages(user_id)
            
            # Process the chat request with full conversation history
            response_text, extracted_data = await chatbot_service.process_chat(all_messages, document_type)
            
            # Create assistant message and add to memory
            assistant_message = Message(role="assistant", content=response_text)
            memory_service.add_message(user_id, assistant_message)
            
            # Update collected data if new data was extracted
            if extracted_data:
                memory_service.update_collected_data(user_id, extracted_data)
        else:
            response_text = "No valid message provided"
        
        # Check if we have enough data to generate PDF
        pdf_generated = False
        
        if memory_service.is_data_complete(user_id):
            # Get the complete collected data
            complete_data = memory_service.get_collected_data(user_id)
            
            # Create a unique filename based on user_id and document_type
            filename = f"{user_id}_{document_type}.pdf"
            
            # Generate PDF with the specific filename
            pdf_path = await pdf_service.fill_pdf(complete_data, filename)
            pdf_generated = True
            
            # If PDF was generated, return it directly
            if pdf_generated:
                response = ChatResponse(
                    response=response_text,
                    user_id=user_id,
                    pdf_generated=pdf_generated
                )
                
                # Return the file as a response
                return FileResponse(
                    path=pdf_path,
                    media_type="application/pdf",
                    filename=filename,
                    headers={"X-Chat-Response": response.json()}
                )
        
        # If no PDF was generated, return the standard JSON response
        return ChatResponse(
            response=response_text,
            user_id=user_id,
            pdf_generated=pdf_generated
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

# Rest of the file remains the same
@router.get("/download/{filename}")
async def download_pdf(filename: str):
    """
    Download a specific generated PDF file
    """
    file_path = os.path.join(pdf_service.output_dir, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PDF file not found")
    
    return FileResponse(file_path, media_type="application/pdf", filename=filename)


@router.delete("/session/{user_id}")
async def clear_session(user_id: str):
    """
    Clear a user's session
    """
    memory_service.clear_session(user_id)
    return {"status": "success", "message": f"Session {user_id} cleared successfully"}

@router.post("/select-document")
async def select_document(user_id: Optional[str] = None, document_type: str = "default"):
    """
    Create a new session or update an existing one with the selected document type
    """
    user_id = memory_service.get_or_create_session(user_id, document_type)
    memory_service.set_document_type(user_id, document_type)
    
    # Return initial message based on document type
    if document_type == "seller_disclosure":
        initial_message = "I'll help you fill out the Seller Property Condition Disclosure Statement. Let's start with some basic information. How old is the house you're selling?"
    else:
        initial_message = "I'll help you fill out the form. Let's start with your name. What's your first and last name?"
    
    return {
        "user_id": user_id,
        "document_type": document_type,
        "initial_message": initial_message
    }

@router.get("/history/{user_id}")
async def get_user_history(user_id: str):
    """
    Retrieve a user's chat history and generated documents
    """
    try:
        # Get user's conversation history
        conversation_history = memory_service.get_messages(user_id)
        return {
            "user_id": user_id,
            "history": conversation_history,
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user history: {str(e)}")