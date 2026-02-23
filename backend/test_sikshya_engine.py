import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault("FLASK_ENV", "testing")

from app.utils.sikshya_engine import run_diagnosis

payload = {
    "sessionId": "S123",
    "studentId": "stu_01",
    "problemTemplate": {
        "id": "PHY_001",
        "steps": [
            {
                "stepNumber": 1,
                "correctAnswer": "Ax = A cos(30) = 8.66 m, Ay = A sin(30) = 5 m",
                "options": [
                    "Ax = A cos(30) = 8.66 m, Ay = A sin(30) = 5 m",
                    "Ax = A sin(30) = 5 m, Ay = A cos(30) = 8.66 m",
                    "Ax = A cos(60) = 5 m, Ay = A sin(60) = 8.66 m",
                    "Ax = Ay = A/2 = 5 m",
                ],
                "explanation": "Horizontal uses cos, vertical uses sin.",
                "commonMisconceptions": ["confusing sin and cos when decomposing"],
            }
        ],
    },
    "studentAnswers": [{"stepNumber": 1, "selectedOptionIndex": 1}],
    "resourcesDB": [
        {"resourceId": "YT_VEC_TRIG_01", "tags": ["trigonometry_vector_decomposition"]},
    ],
}

result = run_diagnosis(payload)
print(json.dumps(result, indent=2))

# Assertions
sr = result["stepResults"][0]
assert sr["correct"] == False, "Should be wrong"
assert sr["inferredPrereqTag"] == "trigonometry_vector_decomposition", \
    f"Expected trig tag, got {sr['inferredPrereqTag']}"
assert sr["confidence"] == "high", f"Expected high, got {sr['confidence']}"
assert "YT_VEC_TRIG_01" in sr["recommendedResourceIds"], "Resource missing"
assert result["nextAction"] == "play_resource", f"Expected play_resource, got {result['nextAction']}"
print("\nALL ASSERTIONS PASSED")
