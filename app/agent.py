import os
from pathlib import Path
import logging
import language_tool_python

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

from .utils import extract_text_from_pdf, extract_text_from_docx, create_modified_docx
from .prompts import COMPLIANCE_CHECK_PROMPT, MODIFICATION_PROMPT

# --- Configuration ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComplianceAgent:
    """
    An AI agent that uses LangChain to check document compliance and suggest modifications.
    """
    def __init__(self):
        # Ensure the API key is set
        if not os.getenv("GEMINI_API_KEY"):
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        
        # Initialize LangChain components
        # Model for JSON output
        self.json_model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest",
            model_kwargs={"response_format": {"type": "json_object"}}
        )
        # Model for standard text output
        self.text_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")
        
        # Initialize LanguageTool for local grammar checks
        try:
            self.lang_tool = language_tool_python.LanguageTool('en-US')
        except Exception as e:
            logger.warning(f"Could not initialize LanguageTool, grammar checks will be skipped. Error: {e}")
            self.lang_tool = None
            
        self.text = ""

    def _parse_document(self, file_path: str):
        """Extracts text from a given document file."""
        file_ext = Path(file_path).suffix.lower()
        if file_ext == ".pdf":
            self.text = extract_text_from_pdf(file_path)
        elif file_ext == ".docx":
            self.text = extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file type.")
        
        if not self.text or not self.text.strip():
            raise ValueError("Could not extract any text from the document.")

    def get_text(self) -> str:
        """Returns the extracted text."""
        return self.text

    def _run_grammar_check(self) -> list:
        """Runs a grammar check using LanguageTool."""
        if not self.lang_tool:
            return []
        matches = self.lang_tool.check(self.text)
        return [
            {
                "ruleId": match.ruleId, "message": match.message, "context": match.context,
                "offset": match.offset, "length": match.errorLength, "replacements": match.replacements
            }
            for match in matches
        ]

    def check_compliance(self, file_path: str) -> dict:
        """
        Checks the document for compliance using a LangChain chain.
        """
        self._parse_document(file_path)
        grammar_errors = self._run_grammar_check()
        
        # Define the prompt template for compliance checking
        prompt_template = ChatPromptTemplate.from_template(COMPLIANCE_CHECK_PROMPT)
        
        # Define the LangChain pipeline (chain)
        chain = prompt_template | self.json_model | JsonOutputParser()
        
        try:
            # Invoke the chain with the required inputs
            report = chain.invoke({
                "document_text": self.text,
                "grammar_errors": grammar_errors
            })
            return report
        except Exception as e:
            logger.error(f"LangChain compliance check failed: {e}")
            raise RuntimeError(f"Failed to get compliance report from AI model: {e}")

    def modify_document(self, original_text: str, report: dict, output_dir: Path, task_id: str) -> str:
        """
        Modifies the document based on the compliance report using a LangChain chain.
        """
        prompt_template = ChatPromptTemplate.from_template(MODIFICATION_PROMPT)
        
        # Define the LangChain pipeline for modification
        chain = prompt_template | self.text_model | StrOutputParser()
        
        try:
            # Invoke the chain
            modified_text = chain.invoke({
                "document_text": original_text,
                "compliance_report": report
            })
            
            # Create a new Word document with the modified text
            output_path = create_modified_docx(modified_text, output_dir, task_id)
            return output_path
        except Exception as e:
            logger.error(f"LangChain modification failed: {e}")
            raise RuntimeError(f"Failed to get modified document from AI model: {e}")