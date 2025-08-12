import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pathlib import Path
import logging

from .agent import ComplianceAgent

# --- Configuration ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="AI Document Compliance Checker (LangChain/Gemini)",
    description="Upload a PDF or Word document to check for compliance against English guidelines using LangChain and Google Gemini.",
    version="1.2.0"
)

# --- In-memory storage for task status and results ---
# In a production environment, use a more robust solution like Redis or a database.
tasks = {}

# --- File Paths & Directories ---
# Create a directory to store uploaded files temporarily
UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
MODIFIED_DIR = Path("modified_docs")
MODIFIED_DIR.mkdir(exist_ok=True)


# --- Background Task for Processing ---
def process_document_task(task_id: str, file_path: str, filename: str):
    """
    Background task to process the document and update the task status.
    """
    try:
        logger.info(f"Starting processing for task_id: {task_id}")
        agent = ComplianceAgent()
        report = agent.check_compliance(file_path)

        tasks[task_id]["status"] = "completed"
        tasks[task_id]["report"] = report
        tasks[task_id]["original_text"] = agent.get_text()
        logger.info(f"Processing completed for task_id: {task_id}")

    except Exception as e:
        logger.error(f"Error processing task {task_id}: {e}", exc_info=True)
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["report"] = {"error": "Failed to process document.", "details": str(e)}


# --- API Endpoints ---

@app.get("/", tags=["General"])
def read_root():
    """A simple endpoint to check if the API is running."""
    return {"message": "Welcome to the AI Document Compliance Checker API (LangChain/Gemini Edition)."}


@app.post("/check-compliance/", status_code=202, tags=["Compliance"])
async def check_compliance(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Accepts a PDF or Word document, processes it, and returns a task ID.
    """
    # Validate file type
    allowed_extensions = {".pdf", ".docx"}
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Please upload a .pdf or .docx file.")

    # Securely save the uploaded file
    task_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{task_id}{file_ext}"

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        logger.info(f"File saved to {file_path}")
    except Exception as e:
        logger.error(f"Could not save file: {e}")
        raise HTTPException(status_code=500, detail="Could not save uploaded file.")

    # Initialize task status
    tasks[task_id] = {"status": "processing", "filename": file.filename}

    # Add the processing task to the background
    background_tasks.add_task(process_document_task, task_id, str(file_path), file.filename)

    return {"task_id": task_id, "message": "Document upload successful. Processing has started."}


@app.get("/results/{task_id}", tags=["Compliance"])
def get_results(task_id: str):
    """
    Retrieves the compliance check results using the task ID.
    """
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")

    return {"task_id": task_id, "status": task["status"], "report": task.get("report")}


@app.post("/modify-document/{task_id}", tags=["Modification"])
async def modify_document(task_id: str):
    """
    Modifies the document to be compliant and returns it for download.
    """
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Document processing is not yet complete.")

    original_text = task.get("original_text")
    if not original_text:
        raise HTTPException(status_code=500, detail="Original text not found for modification.")

    try:
        agent = ComplianceAgent()
        modified_doc_path = agent.modify_document(original_text, task["report"], MODIFIED_DIR, task_id)
        
        # Return the modified document for download
        return FileResponse(
            path=modified_doc_path,
            filename=f"compliant_{task['filename']}.docx",
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except Exception as e:
        logger.error(f"Failed to modify document for task {task_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to modify document: {str(e)}")