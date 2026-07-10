from tfuga.email_business import AITBusinessManager, AITEmailsPublishingManager, CompanyProfile, EmailStatus, Recipient, demo_assets


def test_email_business_managers():
    company = CompanyProfile("X", "x.local", "Tristan", "t@x.local", "Laval, QC")
    ready = AITEmailsPublishingManager().draft(company, Recipient("a@example.com", consent=True), "Hello", "Body")
    blocked = AITEmailsPublishingManager().draft(company, Recipient("b@example.com", consent=False), "Hello", "Body")
    assert ready.status == EmailStatus.READY_FOR_REVIEW
    assert blocked.status == EmailStatus.BLOCKED
    ranked = AITBusinessManager().rank(demo_assets())
    assert ranked[0].name in {"TFUGA Python Library", "Email Publishing Manager"}
