# AI Document Compliance Checker (LangChain/Gemini Edition)

This project is an AI-powered system that processes document files (PDF or Word) and checks their compliance against standard English writing guidelines. It provides a detailed report of violations and can generate a corrected version of the document.

This version has been refactored to use **LangChain** to orchestrate interactions with **Google's Gemini model**, resulting in simpler, more modular code.

## Features

- **API for File Uploads:** A secure FastAPI endpoint to accept `.pdf` and `.docx` files.
- **Asynchronous Processing:** Handles large documents without timing out by processing them in the background.
- **AI-Powered Analysis:** Uses **LangChain** to manage calls to the **Google Gemini API** for nuanced checks on clarity, tone, and sentence structure, supplemented by `language-tool-python` for local grammar/spelling checks.
- **Detailed Compliance Reports:** Generates a structured JSON report detailing all violations and suggestions for improvement.
- **Automated Document Modification:** An endpoint to request an AI-generated, compliant version of the document.
- **Containerized:** Fully containerized with Docker and Docker Compose for easy setup and deployment.

## Technical Stack

- **Backend:** FastAPI
- **Orchestration:** **LangChain**
- **AI/NLP:** **Google Gemini API** (`gemini-1.5-flash`), `language-tool-python`
- **Document Parsing:** `PyMuPDF` (for PDFs), `python-docx` (for Word docs)
- **Testing:** Pytest, HTTPX
- **Containerization:** Docker, Docker Compose

## Setup and Installation

### Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
- A **Google Gemini API key**. You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd document-compliance-checker
    ```

2.  **Configure Environment Variables:**
    Create a `.env` file in the project root.
    Open the `.env` file and add your Gemini API key:
    ```
    GEMINI_API_KEY="your-api-key-here"
    ```

3.  **Build and Run with Docker Compose:**
    From the project root, run the following command:
    ```bash
    docker-compose up --build
    ```
    This will build the Docker image and start the FastAPI application. The API will be accessible at `http://localhost:8000`.

## API Usage

You can interact with the API through its interactive documentation (Swagger UI), available at `http://localhost:8000/docs`. The endpoints and usage patterns remain the same.
```markdown
# /document-compliance-checker/TEST_REPORT.md

# Test Report for AI Document Compliance Checker (LangChain/Gemini Edition)

## 1. Testing Strategy

The system's functionality was validated using a combination of **unit tests** and **integration tests** executed via the `pytest` framework. This version of the report validates the application after refactoring the core AI logic to use the **LangChain** framework for orchestrating calls to the Google Gemini API.

- **Unit Tests:** The principles of unit testing were applied by testing individual API endpoint logic (e.g., handling of invalid file types, non-existent tasks).
- **Integration Tests:** The primary test case, `test_compliance_check_workflow`, covers the entire user journey, ensuring that the LangChain-powered agent correctly processes documents and returns a valid, structured report.

## 2. Test Environment

- **Framework:** Pytest `7.x`
- **HTTP Client:** HTTPX (via `TestClient` from FastAPI)
- **Execution:** Tests were run inside the Docker container to ensure the environment is identical to production.
- **Dependencies:** All dependencies were installed from the updated `requirements.txt`, which now includes `langchain` and `langchain-google-genai`.

## 3. Validation Results

### API Endpoint Tests

The API endpoints remain unchanged and continue to function as expected.

| Endpoint                     | Test Case                     | Status  | Notes                                                                                             |
| ---------------------------- | ----------------------------- | ------- | ------------------------------------------------------------------------------------------------- |
| `GET /`                      | Root endpoint availability    | ✅ Pass | Successfully returns the welcome message, indicating it's the LangChain/Gemini Edition.           |
| `POST /check-compliance/`    | Upload valid `.docx` file     | ✅ Pass | Accepts the file, returns a `202 Accepted` status and a valid `task_id`.                          |
| `POST /check-compliance/`    | Upload invalid `.txt` file    | ✅ Pass | Correctly rejects the file with a `400 Bad Request` error.                                        |
| `GET /results/{task_id}`     | Poll for a valid task         | ✅ Pass | Successfully polls and retrieves the status of the ongoing/completed task.                        |
| `GET /results/{task_id}`     | Request a non-existent task   | ✅ Pass | Returns a `404 Not Found` error as expected.                                                      |

### AI Agent Validation (LangChain)

The agent, now using LangChain, was validated with the same set of sample documents.

| Document Type             | Expected Outcome                                                                                             | Actual Outcome                                                                                                  | Status  |
| ------------------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- | ------- |
| **Non-Compliant Document**| The report should indicate "Non-Compliant" status, a lower score, and a list of identified violations.       | The LangChain-powered agent successfully identified all expected issues. The JSON output parser correctly structured the report. | ✅ Pass |

## 4. Conclusion

The refactoring to incorporate LangChain has been successful. The core logic in `agent.py` is now significantly cleaner and more declarative. By defining chains, we separate the prompt, model, and output parser, which improves maintainability without altering the external behavior of the API. The system remains robust, functional, and meets all project requirements.
