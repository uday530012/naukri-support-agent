from crewai import Agent

from crew.mock_llm import NaukriMockLLM
from crew.tools import (
    search_naukri_knowledge_base,
    check_job_application_status,
)


# ============================================================
# MOCK LLM
# ============================================================

mock_llm = NaukriMockLLM()


# ============================================================
# 1. RETRIEVAL AGENT
# ============================================================

retrieval_agent = Agent(
    role="Naukri Knowledge Retrieval Agent",
    goal=(
        "Retrieve accurate, relevant information from the Naukri "
        "knowledge base for recruitment and job-application questions."
    ),
    backstory=(
        "You are a knowledge retrieval specialist for Naukri support. "
        "You must rely on the provided knowledge-base tool and avoid "
        "inventing policies or unsupported information."
    ),
    tools=[search_naukri_knowledge_base],
    llm=mock_llm,
    verbose=True,
    allow_delegation=False,
)


# ============================================================
# 2. LOOKUP AGENT
# ============================================================

lookup_agent = Agent(
    role="Naukri Application Lookup Agent",
    goal=(
        "Check specific Naukri job application records and provide "
        "accurate application status and escalation information."
    ),
    backstory=(
        "You are an application-status specialist. You use the "
        "application lookup tool when a user provides an application "
        "record ID such as APP1001."
    ),
    tools=[check_job_application_status],
    llm=mock_llm,
    verbose=True,
    allow_delegation=False,
)


# ============================================================
# 3. RESPONSE COMPOSER
# ============================================================

response_composer = Agent(
    role="Naukri Support Response Composer",
    goal=(
        "Create a concise, accurate and grounded final response "
        "using the information supplied by the retrieval and lookup "
        "agents."
    ),
    backstory=(
        "You are the final response specialist for Naukri customer "
        "support. Never invent information. Use only the evidence "
        "provided by the other agents and clearly state when the "
        "available evidence is insufficient."
    ),
    tools=[],
    llm=mock_llm,
    verbose=True,
    allow_delegation=False,
)