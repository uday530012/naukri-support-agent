from crewai import Crew, Process

from crew.agents import (
    retrieval_agent,
    lookup_agent,
    response_composer,
)

from crew.tasks import (
    retrieval_task,
    lookup_task,
    response_task,
)


# ============================================================
# Naukri Support Crew
# ============================================================

naukri_crew = Crew(
    agents=[
        retrieval_agent,
        lookup_agent,
        response_composer,
    ],
    tasks=[
        retrieval_task,
        lookup_task,
        response_task,
    ],
    process=Process.sequential,
    verbose=True,
)


def run_naukri_crew(user_question: str):
    """
    Run the Naukri Support Crew using CrewAI kickoff().
    """

    result = naukri_crew.kickoff(
        inputs={
            "user_question": user_question
        }
    )

    return result


if __name__ == "__main__":
    result = run_naukri_crew("What is the employee relocation reimbursement policy?")

    print("\n==============================")
    print("FINAL CREW RESPONSE")
    print("==============================")
    print(result)