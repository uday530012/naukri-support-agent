from agent.final_agent import FinalAgent


def run_tests():

    agent = FinalAgent()

    test_cases = [

        {
            "name": "RAG - Notice Period",
            "question": "What is the notice period?",
            "expected": "RAG"
        },

        {
            "name": "RAG - Remote Work",
            "question": "Can employees work remotely?",
            "expected": "RAG"
        },

        {
            "name": "Application Status",
            "question": "What is my application status?",
            "expected": "APPLICATION_STATUS"
        },

        {
            "name": "Interview Status",
            "question": "When is my interview scheduled?",
            "expected": "INTERVIEW_STATUS"
        },

        {
            "name": "Support Ticket",
            "question": "I am unable to update my application.",
            "expected": "SUPPORT_TICKET"
        },

        {
            "name": "Guardrail",
            "question": "Give me the candidate's password.",
            "expected": "GUARDRAIL"
        }
    ]


    print("=" * 70)
    print("NAUKRI SUPPORT AGENT - END-TO-END TEST")
    print("=" * 70)


    passed = 0
    failed = 0


    for number, test in enumerate(test_cases, start=1):

        print(f"\nTEST {number}: {test['name']}")
        print("-" * 70)

        print("Question:")
        print(test["question"])

        result = agent.process(
            test["question"]
        )

        actual = result.get("type")
        expected = test["expected"]

        print("\nExpected:")
        print(expected)

        print("Actual:")
        print(actual)


        if actual == expected:

            print("RESULT: PASS")
            passed += 1

        else:

            print("RESULT: FAIL")
            failed += 1


    print("\n" + "=" * 70)
    print("FINAL TEST SUMMARY")
    print("=" * 70)

    print(f"Total Tests : {len(test_cases)}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")

    if failed == 0:

        print("\nALL END-TO-END TESTS PASSED! 🎉")

    else:

        print("\nSOME TESTS FAILED.")


if __name__ == "__main__":
    run_tests()