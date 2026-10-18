from crewai import Task

from crew.agents import (
    retrieval_agent,
    lookup_agent,
    response_composer,
)

from crew.schemas import NaukriSupportResponse


# ============================================================
# 1. RETRIEVAL TASK
# ============================================================

retrieval_task = Task(
    description=(
        "Analyze the following user's question:\n\n"
        "{user_question}\n\n"
        "Retrieve the relevant Naukri policy or recruitment "
        "information for this question. "
        "Use the search_naukri_knowledge_base tool when appropriate. "
        "Return only information supported by the knowledge base. "
        "Do not invent policies, requirements, or facts."
    ),
    expected_output=(
        "A concise evidence summary containing the relevant "
        "Naukri policy information supported by the knowledge base."
    ),
    agent=retrieval_agent,
)


# ============================================================
# 2. APPLICATION LOOKUP TASK
# ============================================================

lookup_task = Task(
    description=(
        "Analyze the following user's question:\n\n"
        "{user_question}\n\n"
        "Determine whether the user has provided a Naukri "
        "application record ID such as APP1001, APP1002, or APP1003. "
        "If an application ID is present, use the "
        "check_job_application_status tool to retrieve the "
        "application status, expected salary, application age, "
        "priority flag, escalation score, and priority-review "
        "recommendation. "
        "If no application ID is present, state that application "
        "lookup is not required."
    ),
    expected_output=(
        "A concise application lookup result containing the "
        "application information when an application ID is present, "
        "or a statement that application lookup is not required."
    ),
    agent=lookup_agent,
)


# ============================================================
# 3. RESPONSE COMPOSER TASK
# ============================================================

response_task = Task(
    description=(
        "Answer the following user's question:\n\n"
        "{user_question}\n\n"
        "Create the final Naukri support response using the evidence "
        "provided by the retrieval and application lookup tasks. "
        "Answer the user's actual question directly. "
        "Do not answer a different topic merely because related "
        "words appear in the task instructions. "
        "Do not invent information. "
        "Use only information supported by the available evidence. "
        "If the evidence is insufficient, clearly state that the "
        "available information is insufficient.\n\n"
        "The final response MUST contain these four fields:\n"
        "1. status\n"
        "2. response\n"
        "3. source\n"
        "4. next_action"
    ),
    expected_output=(
        "A structured Naukri support response containing status, "
        "response, source, and next_action."
    ),
    agent=response_composer,
    output_pydantic=NaukriSupportResponse,
)