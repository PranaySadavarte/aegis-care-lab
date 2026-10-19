"""Small reviewed SDK reference. Never inject account records into answers."""
TOPICS = {
    "task": "Guava tasks define an objective and checklist. Fields collect structured values, and on_task_complete runs backend work. Task completion is not proof of authorization.",
    "sensitive": "Sensitive fields mark data for special handling. Our prior hosted text tests retained caller test values in transcripts, so this flag is not proof of redaction. Only synthetic card fixtures are allowed here.",
    "card": "Choose payments, consent to simulation, then choose synthetic_card. The designated test PAN and CVV travel through Guava fields to a local fixture validator. Only last four and status enter the outcome. There is no payment gateway or real charge.",
    "roleplay": "Guava Agent.test opens a hosted text session; set_persona and roleplay simulate callers. Validate that the actor followed its instructions before grading the target. Native evaluate is supplementary to backend assertions.",
    "audio": "Guava supports prerecorded test_audio, WebRTC, local audio, and phone listeners. Text success does not prove ASR, pronunciation, interruption handling, or carrier routing.",
    "transfer": "The SDK supports transfer, reach_person, DTMF, and telephony callbacks. This demo has no human destination configured. Those features need separate mocked contracts and authorized integration tests.",
    "sdk": "This lab targets Guava SDK 0.47.0. It uses tasks, typed sensitive fields, action and question callbacks, validation, searchable appointment fields, DatetimeFilter, caller speech, escalation, session cleanup and hosted testing. Transport and external integrations have separate coverage limits.",
}
def answer_sdk_question(question):
    text=question.lower()
    if not any(word in text for word in ("sdk","guava","test","feature","card","sensitive","roleplay")):
        return None
    for key,value in TOPICS.items():
        if key in text:return value
    return TOPICS["sdk"]
