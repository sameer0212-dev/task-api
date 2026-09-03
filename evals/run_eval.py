import json
import requests

API_URL = "http://localhost:8000/enrich"

def run_eval():
    with open("evals/cases.json") as f:
        cases = json.load(f)

    passed = 0
    total = len(cases)

    print(f"Running evaluation on {total} test cases...\n")

    for idx, case in enumerate(cases, 1):
        response = requests.post(API_URL, json=case["input"])
        data = response.json()
        category = data.get("category")
        
        is_match = (category == case["expected_category"])
        if is_match:
            passed += 1
            status = "PASS"
        else:
            status = f"FAIL (Expected: {case['expected_category']}, Got: {category})"

        print(f"Case {idx}: [{status}] - {case['input']['title']}")

    score = (passed / total) * 100
    print(f"\nFinal Eval Score: {passed}/{total} ({score:.1f}%)")

if __name__ == "__main__":
    run_eval()