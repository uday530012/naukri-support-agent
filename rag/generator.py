import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


MODEL_NAME = "gemini-2.5-flash"


class AnswerGenerator:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        print(
            f"Gemini model loaded: {MODEL_NAME}"
        )

    def generate_answer(
        self,
        question,
        context
    ):
        """
        Generate an answer using only the
        retrieved policy context.
        """

        prompt = f"""
You are a Naukri.com Job Application Support Agent.

Answer the user's question using ONLY the
policy information provided in the context.

Do not invent information.

If the context does not contain enough information
to answer the question, clearly say:

"I could not find enough information in the
available policy documents."

Be concise, professional, and helpful.

CONTEXT:
--------------------
{context}
--------------------

USER QUESTION:
{question}

ANSWER:
"""

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text


if __name__ == "__main__":

    generator = AnswerGenerator()

    test_question = (
        "What is the notice period policy?"
    )

    test_context = """
    Employees are expected to follow the notice
    period specified in their employment terms.
    """

    answer = generator.generate_answer(
        test_question,
        test_context
    )

    print("\n" + "=" * 60)
    print("GEMINI ANSWER TEST")
    print("=" * 60)

    print("\nQuestion:")
    print(test_question)

    print("\nAnswer:")
    print(answer)
