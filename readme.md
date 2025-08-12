# Compliance Validator

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
