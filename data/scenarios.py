SCENARIOS = [
    {
        "id": 1,
        "intent": "Follow up after a sales meeting",
        "key_facts": [
            "Meeting held on Tuesday at 10 AM",
            "Client is interested in the Enterprise plan",
            "Pricing proposal to be sent by Thursday",
            "Next call scheduled for Monday"
        ],
        "tone": "formal",
        "reference_email": """Subject: Follow-Up: Our Meeting on Tuesday & Next Steps

Dear [Client Name],

Thank you for taking the time to meet with us this Tuesday at 10 AM. It was a pleasure discussing your needs and how our Enterprise plan could support your goals.

As discussed, I will have the detailed pricing proposal ready and sent to you by Thursday. I look forward to connecting again on Monday to walk you through the proposal and answer any questions you may have.

Please don't hesitate to reach out in the meantime if you need any information.

Best regards,
[Your Name]"""
    },
    {
        "id": 2,
        "intent": "Request an extension on a project deadline",
        "key_facts": [
            "Original deadline is this Friday",
            "Team member fell ill, causing delays",
            "Requesting a 5-day extension",
            "Will provide a progress update by Wednesday"
        ],
        "tone": "formal",
        "reference_email": """Subject: Request for Project Deadline Extension

Dear [Manager's Name],

I am writing to formally request a short extension on our current project, which is due this Friday. Unfortunately, one of our key team members has fallen ill, which has caused unexpected delays in our progress.

To ensure we deliver the quality of work you expect, I would like to request a 5-day extension on the deadline. I will provide a detailed progress update by Wednesday so you have full visibility into where we stand.

I apologize for any inconvenience this may cause and appreciate your understanding.

Sincerely,
[Your Name]"""
    },
    {
        "id": 3,
        "intent": "Welcome a new team member",
        "key_facts": [
            "New hire's name is Sarah",
            "She is joining as a Data Analyst",
            "Start date is next Monday",
            "Team lunch planned for Tuesday at noon"
        ],
        "tone": "friendly",
        "reference_email": """Subject: Welcome to the Team, Sarah!

Hi everyone,

I'm thrilled to announce that Sarah will be joining us as our new Data Analyst starting next Monday! She brings a great set of skills and we're so excited to have her on board.

To give Sarah a warm welcome, we've planned a team lunch this Tuesday at noon — mark your calendars! It'll be a great chance to get to know her and kick things off on a fun note.

Please join me in welcoming Sarah to the team. See you all Tuesday!

Cheers,
[Your Name]"""
    },
    {
        "id": 4,
        "intent": "Notify a client about a service outage",
        "key_facts": [
            "Outage started at 3 AM EST",
            "Affects the payment processing module",
            "Engineering team is actively working on it",
            "Estimated resolution time is 4 hours"
        ],
        "tone": "empathetic",
        "reference_email": """Subject: Important: Service Disruption Affecting Payment Processing

Dear Valued Customer,

We want to reach out and sincerely apologize for the service disruption you may be experiencing. At 3 AM EST, we identified an outage affecting our payment processing module, and we understand how critical this is to your operations.

Our engineering team is actively working on a fix and we estimate the service will be fully restored within 4 hours. We are treating this as our highest priority.

We are truly sorry for the inconvenience and will keep you updated on our progress. Thank you for your patience and understanding.

Warm regards,
[Support Team]"""
    },
    {
        "id": 5,
        "intent": "Request a recommendation letter",
        "key_facts": [
            "Applying for an MBA program at Harvard",
            "Deadline for the letter is December 1st",
            "Worked together for 3 years",
            "Will share CV and personal statement for reference"
        ],
        "tone": "formal",
        "reference_email": """Subject: Request for a Letter of Recommendation

Dear [Professor/Manager Name],

I hope this message finds you well. I am writing to respectfully ask if you would be willing to write a letter of recommendation for my MBA application to Harvard Business School.

Having had the privilege of working with you for the past three years, I believe you are uniquely positioned to speak to my skills and character. The deadline for the letter submission is December 1st.

To make this as easy as possible for you, I will share my updated CV and personal statement for your reference. I would be honored to have your support in this next step of my journey.

Thank you so much for considering this request.

Sincerely,
[Your Name]"""
    },
    {
        "id": 6,
        "intent": "Escalate an unresolved customer complaint",
        "key_facts": [
            "Customer has been waiting for a refund for 3 weeks",
            "Two previous support tickets were not resolved",
            "Order number is #78432",
            "Customer is threatening to leave a public review"
        ],
        "tone": "urgent",
        "reference_email": """Subject: URGENT: Unresolved Refund for Order #78432 — Immediate Action Required

Dear [Manager's Name],

I need to bring an urgent matter to your immediate attention. A customer has been waiting for a refund on Order #78432 for over three weeks, and despite two previous support tickets, the issue remains unresolved.

The customer is now expressing frustration and has indicated they may share their experience publicly if this is not addressed immediately. We need to act now to prevent further escalation.

I am requesting your direct intervention to ensure this refund is processed today. Please advise on the next steps as soon as possible.

Thank you,
[Your Name]"""
    },
    {
        "id": 7,
        "intent": "Invite stakeholders to a product demo",
        "key_facts": [
            "Demo is on Thursday at 3 PM",
            "Showcasing the new analytics dashboard",
            "Session will last 45 minutes",
            "Zoom link will be shared separately"
        ],
        "tone": "friendly",
        "reference_email": """Subject: You're Invited: New Analytics Dashboard Demo — Thursday at 3 PM

Hi Team,

We'd love to have you join us for an exclusive demo of our brand-new Analytics Dashboard this Thursday at 3 PM!

The session will run for about 45 minutes and we'll be walking through all the exciting new features we've been building. It's a great opportunity to see everything in action and share your feedback.

A Zoom link will be on its way to you shortly. We hope to see you there!

Best,
[Your Name]"""
    },
    {
        "id": 8,
        "intent": "Apologize for missing a deadline",
        "key_facts": [
            "The report was due last Friday",
            "Delay caused by unexpected data discrepancies",
            "Report will be delivered by tomorrow EOD",
            "Steps being taken to prevent future delays"
        ],
        "tone": "empathetic",
        "reference_email": """Subject: Apology for Delayed Report Submission

Dear [Recipient Name],

I want to sincerely apologize for not delivering the report by last Friday as committed. I understand this may have caused disruption to your planning and I take full responsibility.

The delay was caused by unexpected data discrepancies that required additional time to resolve accurately. I can confirm the final report will be in your hands by tomorrow end of day.

I am also reviewing our internal process to ensure this does not happen again. Thank you for your patience, and I am sorry for the inconvenience.

Best regards,
[Your Name]"""
    },
    {
        "id": 9,
        "intent": "Negotiate a contract renewal with a vendor",
        "key_facts": [
            "Current contract expires in 30 days",
            "Requesting a 15% price reduction",
            "Willing to commit to a 2-year contract",
            "Competitor has offered a better rate"
        ],
        "tone": "assertive",
        "reference_email": """Subject: Contract Renewal Discussion — Proposed Terms

Dear [Vendor Name],

As our current contract is set to expire in 30 days, I'd like to open discussions on the terms of our renewal.

We value our partnership, and we are prepared to commit to a 2-year contract to reflect our long-term intent. However, to proceed, we need to discuss a 15% reduction in the current pricing. I want to be transparent — we have received a competitive offer from another vendor, and aligning on pricing is essential for us to continue this relationship.

I am confident we can find a mutually beneficial arrangement. Please let me know your availability for a call this week.

Regards,
[Your Name]"""
    },
    {
        "id": 10,
        "intent": "Announce a company policy change",
        "key_facts": [
            "New remote work policy effective from January 1st",
            "Employees must be in office 3 days per week",
            "Policy applies to all non-field staff",
            "HR will host a Q&A session on December 15th"
        ],
        "tone": "formal",
        "reference_email": """Subject: Important Update: Revised Remote Work Policy Effective January 1st

Dear Team,

I am writing to inform you of an important update to our remote work policy, effective January 1st.

Beginning in the new year, all non-field staff will be required to work from the office a minimum of three days per week. This change reflects our commitment to fostering collaboration and maintaining a strong team culture.

We understand you may have questions, and our HR team will be hosting a dedicated Q&A session on December 15th to address them. Further details about the session will follow shortly.

We appreciate your continued dedication and cooperation as we make this transition.

Sincerely,
[Leadership Team]"""
    }
]