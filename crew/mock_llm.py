import json
import re
from typing import Any

from crewai.llms.base_llm import BaseLLM


class NaukriMockLLM(BaseLLM):
    """
    Deterministic MOCK_LLM for the Naukri Support Agent.

    No API calls.
    No API key.
    Deterministic responses.
    Supports Pydantic structured output.
    """

    def __init__(self, temperature: float = 0.0):
        super().__init__(
            model="naukri-mock-llm",
            temperature=temperature,
        )

    # ============================================================
    # EXTRACT ONLY THE ACTUAL USER QUESTION
    # ============================================================

    def _extract_user_question(self, text: str) -> str:
        """
        Extract the actual user question from CrewAI's prompt.

        Important:
        Do not allow examples such as APP1001/APP1002/APP1003
        appearing in task instructions to become the question.
        """

        patterns = [
            r"Analyze the following user's question:\s*\n+(.*?)\n+Determine",
            r"Answer the following user's question:\s*\n+(.*?)\n+Create",
            r"Analyze the following user's question:\s*\n+(.*?)\n+Retrieve",
        ]

        for pattern in patterns:
            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE | re.DOTALL,
            )

            if match:
                question = match.group(1).strip()

                # Remove accidental whitespace/newlines
                question = re.sub(r"\s+", " ", question)

                return question

        # Fallback: look for a clearly formatted user question
        fallback_patterns = [
            r"user_question\s*[:=]\s*(.*?)(?:\n|$)",
            r"Current question:\s*(.*?)(?:\n|$)",
        ]

        for pattern in fallback_patterns:
            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE | re.DOTALL,
            )

            if match:
                return re.sub(r"\s+", " ", match.group(1).strip())

        return text.strip()

    # ============================================================
    # STRUCTURED RESPONSE
    # ============================================================

    def _structured_response(
        self,
        response: str,
        source: str = "Knowledge Base",
        next_action: str = "Review the relevant Naukri information.",
        status: str = "success",
    ) -> str:

        result = {
            "status": status,
            "response": response,
            "source": source,
            "next_action": next_action,
        }

        return json.dumps(result)

    # ============================================================
    # MAIN LLM CALL
    # ============================================================

    def call(
        self,
        messages: Any,
        tools: Any = None,
        callbacks: Any = None,
        available_functions: Any = None,
        from_task: Any = None,
        from_agent: Any = None,
        response_model: Any = None,
        **kwargs: Any,
    ) -> str:

        # Convert CrewAI messages to text
        if isinstance(messages, list):
            text = "\n".join(
                str(message.get("content", ""))
                if isinstance(message, dict)
                else str(message)
                for message in messages
            )
        else:
            text = str(messages)

        # Extract ONLY the actual user question
        user_question = self._extract_user_question(text)
        text_lower = user_question.lower()

        # ========================================================
        # APPLICATION LOOKUP
        # ========================================================

        if re.search(r"\bAPP1001\b", user_question, re.IGNORECASE):
            response = (
                "Application APP1001 is currently Applied. "
                "The expected salary is ₹600000. "
                "The application was created 5 days ago and is not "
                "currently flagged for priority review."
            )

            if response_model is not None:
                return self._structured_response(
                    response=response,
                    source="Application Status Tool",
                    next_action="Continue monitoring the application status.",
                )

            return response

        if re.search(r"\bAPP1002\b", user_question, re.IGNORECASE):
            response = (
                "Application APP1002 is currently Interview Scheduled. "
                "The expected salary is ₹900000. "
                "The application was created 12 days ago and is "
                "flagged for priority review."
            )

            if response_model is not None:
                return self._structured_response(
                    response=response,
                    source="Application Status Tool",
                    next_action="Review the scheduled interview details.",
                )

            return response

        if re.search(r"\bAPP1003\b", user_question, re.IGNORECASE):
            response = (
                "Application APP1003 is currently in Screening. "
                "The expected salary is ₹750000. "
                "The application was created 18 days ago and is not "
                "currently flagged for priority review."
            )

            if response_model is not None:
                return self._structured_response(
                    response=response,
                    source="Application Status Tool",
                    next_action="Continue monitoring the application status.",
                )

            return response

        # ========================================================
        # NOTICE PERIOD
        # ========================================================

        if "notice period" in text_lower:
            response = (
                "Based on the Naukri knowledge base, notice-period "
                "requirements depend on the employer and role. "
                "Candidates should review the specific job posting "
                "and employer requirements."
            )

            if response_model is not None:
                return self._structured_response(
                    response=response,
                    source="Knowledge Base",
                    next_action="Check the specific job posting.",
                )

            return response

        # ========================================================
        # REMOTE WORK
        # ========================================================

        if (
            "remote work" in text_lower
            or "work from home" in text_lower
        ):
            response = (
                "Remote-work availability depends on the employer "
                "and the specific job role. Please check the job "
                "posting for the applicable work arrangement."
            )

            if response_model is not None:
                return self._structured_response(
                    response=response,
                    source="Knowledge Base",
                    next_action="Check the job posting for the work arrangement.",
                )

            return response

        # ========================================================
        # INTERVIEW
        # ========================================================

        if "interview" in text_lower:
            response = (
                "Interview scheduling depends on the employer's "
                "recruitment process. Candidates should follow the "
                "interview instructions provided for their application."
            )

            if response_model is not None:
                return self._structured_response(
                    response=response,
                    source="Knowledge Base",
                    next_action="Follow the interview instructions for the application.",
                )

            return response

        # ========================================================
        # BACKGROUND VERIFICATION
        # ========================================================

        if "background verification" in text_lower:
            response = (
                "Background verification may be part of the hiring "
                "process. The employer may verify information relevant "
                "to the role before completing the hiring process."
            )

            if response_model is not None:
                return self._structured_response(
                    response=response,
                    source="Knowledge Base",
                    next_action="Review the employer's verification requirements.",
                )

            return response

        # ========================================================
        # REFERRAL
        # ========================================================

        if "referral" in text_lower:
            response = (
                "Referral benefits depend on the applicable referral "
                "policy and eligibility requirements."
            )

            if response_model is not None:
                return self._structured_response(
                    response=response,
                    source="Knowledge Base",
                    next_action="Check the applicable referral policy.",
                )

            return response

        # ========================================================
        # OFFER NEGOTIATION
        # ========================================================

        if (
            "offer negotiation" in text_lower
            or "negotiate" in text_lower
        ):
            response = (
                "Offer negotiation depends on the employer's hiring "
                "policy and the terms of the offer. Candidates should "
                "discuss applicable terms directly with the employer."
            )

            if response_model is not None:
                return self._structured_response(
                    response=response,
                    source="Knowledge Base",
                    next_action="Discuss applicable terms with the employer.",
                )

            return response

        # ========================================================
        # PROBATION
        # ========================================================

        if "probation" in text_lower:
            response = (
                "Probation terms depend on the employer and role. "
                "Candidates should review the employment terms provided "
                "by the employer."
            )

            if response_model is not None:
                return self._structured_response(
                    response=response,
                    source="Knowledge Base",
                    next_action="Review the employment terms provided by the employer.",
                )

            return response

        # ========================================================
        # INTERNAL TRANSFER
        # ========================================================

        if "internal transfer" in text_lower:
            response = (
                "Internal-transfer eligibility depends on the employer's "
                "internal mobility policy and the employee's eligibility."
            )

            if response_model is not None:
                return self._structured_response(
                    response=response,
                    source="Knowledge Base",
                    next_action="Check the employer's internal mobility policy.",
                )

            return response

        # ========================================================
        # DIVERSITY HIRING
        # ========================================================

        if "diversity" in text_lower:
            response = (
                "Diversity hiring policies depend on the employer's "
                "recruitment practices and applicable requirements."
            )

            if response_model is not None:
                return self._structured_response(
                    response=response,
                    source="Knowledge Base",
                    next_action="Review the employer's recruitment policy.",
                )

            return response

        # ========================================================
        # EXIT INTERVIEW
        # ========================================================

        if "exit interview" in text_lower:
            response = (
                "An exit interview is a discussion conducted when an "
                "employee leaves an organization to collect feedback "
                "about their employment experience."
            )

            if response_model is not None:
                return self._structured_response(
                    response=response,
                    source="Knowledge Base",
                    next_action="Review the employer's exit process.",
                )

            return response

        # ========================================================
        # APPLICANT DATA RETENTION
        # ========================================================

        if (
            "applicant data" in text_lower
            or "data retention" in text_lower
        ):
            response = (
                "Applicant-data retention is governed by the applicable "
                "recruitment and data-retention policy."
            )

            if response_model is not None:
                return self._structured_response(
                    response=response,
                    source="Knowledge Base",
                    next_action="Review the applicable data-retention policy.",
                )

            return response

        # ========================================================
        # JOB APPLICATION / ELIGIBILITY
        # ========================================================

        if (
            "job application" in text_lower
            or "eligibility" in text_lower
        ):
            response = (
                "Job-application eligibility depends on the requirements "
                "specified for the particular job posting."
            )

            if response_model is not None:
                return self._structured_response(
                    response=response,
                    source="Knowledge Base",
                    next_action="Review the requirements in the job posting.",
                )

            return response

        # ========================================================
        # GROUNDEDNESS REFUSAL / SAFE FALLBACK
        # ========================================================

        response = (
            "I cannot provide a reliable answer because the available "
            "Naukri knowledge base does not contain sufficient evidence "
            "for this question."
        )

        if response_model is not None:
            return self._structured_response(
                response=response,
                source="Insufficient Evidence",
                next_action="Provide a question covered by the Naukri knowledge base.",
                status="fallback",
            )

        return response

    # ============================================================
    # CREWAI CAPABILITIES
    # ============================================================

    def supports_function_calling(self) -> bool:
        return False

    def supports_stop_words(self) -> bool:
        return False

    def get_context_window_size(self) -> int:
        return 4096

    async def acall(self, messages: Any, **kwargs: Any) -> str:
        return self.call(messages, **kwargs)