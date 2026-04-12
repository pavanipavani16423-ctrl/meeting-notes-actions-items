import json
import re

def parse_output(response_text):
    actions = []

    # 🔹 Try JSON extraction first
    try:
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
            actions = data.get("actions", [])
    except:
        pass

    # 🔹 STRONG fallback (line-based extraction)
    if not actions:
        lines = response_text.split("\n")

        for line in lines:
            line = line.strip()

            if not line:
                continue

            # 🔥 Detect any meaningful task sentence
            if any(word in line.lower() for word in ["will", "prepare", "complete", "finish", "review", "update", "test"]):

                task = line

                # Extract owner (first word if capitalized)
                words = task.split()
                owner = words[0] if words else "not_available"

                # Extract deadline
                if "by" in line.lower():
                    deadline = line.split("by")[-1].strip().replace(".", "")
                elif "before" in line.lower():
                    deadline = line.split("before")[-1].strip().replace(".", "")
                else:
                    deadline = "not_available"

                # Priority logic
                priority = "High" if deadline != "not_available" else "Medium"

                actions.append({
                    "task": task,
                    "owner": owner,
                    "deadline": deadline,
                    "priority": priority
                })

    return {"actions": actions}