class NaukriTools:

    def __init__(self):

        # Mock application database
        self.applications = {
            "APP1001": {
                "candidate": "Candidate 1",
                "job": "Python Developer",
                "status": "Under Review"
            },
            "APP1002": {
                "candidate": "Candidate 2",
                "job": "AI Engineer",
                "status": "Interview Scheduled"
            },
            "APP1003": {
                "candidate": "Candidate 3",
                "job": "Robotics Engineer",
                "status": "Application Submitted"
            }
        }

        # Mock interview database
        self.interviews = {
            "APP1002": {
                "date": "2026-10-20",
                "time": "11:00 AM",
                "mode": "Online",
                "status": "Scheduled"
            }
        }

        # Support tickets
        self.tickets = []

    def check_application_status(self, application_id):

        application = self.applications.get(application_id)

        if application is None:

            return {
                "success": False,
                "message": "Application ID not found."
            }

        return {
            "success": True,
            "application_id": application_id,
            "candidate": application["candidate"],
            "job": application["job"],
            "status": application["status"]
        }

    def check_interview_status(self, application_id):

        interview = self.interviews.get(application_id)

        if interview is None:

            return {
                "success": False,
                "message": "No interview information found."
            }

        return {
            "success": True,
            "application_id": application_id,
            "date": interview["date"],
            "time": interview["time"],
            "mode": interview["mode"],
            "status": interview["status"]
        }

    def create_support_ticket(self, issue):

        ticket_id = f"TICKET{len(self.tickets) + 1001}"

        ticket = {
            "ticket_id": ticket_id,
            "issue": issue,
            "status": "Open"
        }

        self.tickets.append(ticket)

        return {
            "success": True,
            "ticket_id": ticket_id,
            "issue": issue,
            "status": "Open"
        }


def main():

    tools = NaukriTools()

    print("=" * 70)
    print("NAUKRI SUPPORT AGENT - TOOLS TEST")
    print("=" * 70)

    # Test 1: Application status
    print("\n1. APPLICATION STATUS")
    print("-" * 70)

    result = tools.check_application_status("APP1001")

    print(result)

    # Test 2: Interview status
    print("\n2. INTERVIEW STATUS")
    print("-" * 70)

    result = tools.check_interview_status("APP1002")

    print(result)

    # Test 3: Create support ticket
    print("\n3. SUPPORT TICKET")
    print("-" * 70)

    result = tools.create_support_ticket(
        "Unable to update my application details."
    )

    print(result)

    # Test 4: Invalid application
    print("\n4. INVALID APPLICATION")
    print("-" * 70)

    result = tools.check_application_status("APP9999")

    print(result)


if __name__ == "__main__":
    main()