COMPLIANCE_CHECK_PROMPT = """
You are an AI assistant tasked with checking a document for compliance with standard English writing guidelines.
The guidelines focus on:
1.  **Grammar and Spelling:** Correctness of grammar, punctuation, and spelling.
2.  **Clarity:** The text should be clear, concise, and easy to understand. Avoid jargon and overly complex sentences.
3.  **Sentence Structure:** Use a variety of sentence structures. Prefer active voice over passive voice.
4.  **Tone:** Maintain a professional and objective tone.

**Input Document Text:**
---
{document_text}
---

**Initial Grammar/Spelling Errors (from LanguageTool):**
---
{grammar_errors}
---

**Your Task:**
Review the document text and the initial list of grammar errors. Generate a detailed compliance report in JSON format.
The JSON report should have the following structure:
{{
  "summary": {{
    "compliance_status": "Compliant" | "Non-Compliant",
    "overall_score": <a float between 0.0 and 1.0 representing overall compliance>,
    "key_findings": "<A brief summary of the main issues found or a statement of compliance.>"
  }},
  "violations": [
    {{
      "type": "Grammar" | "Clarity" | "Sentence Structure" | "Tone",
      "description": "<A clear description of the violation.>",
      "context": "<The snippet of text where the violation occurred.>",
      "suggestion": "<A concrete suggestion for how to fix the issue.>"
    }}
  ]
}}

- If no violations are found, the "violations" array should be empty and the status should be "Compliant".
- Consolidate the initial grammar errors into the final report.
- Analyze the text for higher-level issues like clarity, passive voice, and tone that a simple grammar checker might miss.

Provide only the JSON report. Do not add markdown formatting like ```json.
"""

MODIFICATION_PROMPT = """
You are an AI assistant tasked with modifying a document to make it fully compliant with standard English writing guidelines.

**Original Document Text:**
---
{document_text}
---

**Compliance Report (Issues to fix):**
---
{compliance_report}
---

**Your Task:**
Rewrite the entire document to fix all the issues listed in the compliance report.
The revised document must:
- Correct all grammar and spelling mistakes.
- Improve clarity and conciseness.
- Convert passive voice to active voice where appropriate.
- Ensure a professional and consistent tone.
- Preserve the original meaning and intent of the text.

Provide only the full, rewritten, and compliant text of the document. Do not include any explanations or introductory phrases.
"""