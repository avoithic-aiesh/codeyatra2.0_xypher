"""HTTP-layer test for POST /api/sikshya/diagnose"""
import json
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

app = create_app()
client = app.test_client()

payload = {
    "sessionId": "S123",
    "studentId": "stu_01",
    "problemTemplate": {
        "id": "PHY_001",
        "steps": [{
            "stepNumber": 1,
            "correctAnswer": "Ax = A cos(30)",
            "options": [
                "Ax = A cos(30)",
                "Ax = A sin(30), Ay = A cos(30)",
                "option3",
                "option4",
            ],
            "explanation": "Horizontal uses cos.",
            "commonMisconceptions": [],
        }],
    },
    "studentAnswers": [{"stepNumber": 1, "selectedOptionIndex": 1}],
    "resourcesDB": [{"resourceId": "YT1", "tags": ["trigonometry_vector_decomposition"]}],
}

r = client.post(
    "/api/sikshya/diagnose",
    data=json.dumps(payload),
    content_type="application/json",
)
print("Status:", r.status_code)
data = r.get_json()
assert data["success"] is True, f"Expected success=True, got: {data}"
assert data["data"]["nextAction"] == "play_resource"
assert data["data"]["stepResults"][0]["inferredPrereqTag"] == "trigonometry_vector_decomposition"
print("nextAction:", data["data"]["nextAction"])
print("tag:", data["data"]["stepResults"][0]["inferredPrereqTag"])
print("HTTP route OK")
