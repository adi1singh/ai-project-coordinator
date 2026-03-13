import json
from openai import OpenAI
from prompts import EXTRACTION_PROMPT, SUMMARY_PROMPT


def extract_tasks_from_notes(meeting_notes, api_key):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You extract structured project tasks from meeting notes."
            },
            {
                "role": "user",
                "content": EXTRACTION_PROMPT + "\n" + meeting_notes
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    try:
        tasks = json.loads(content)
        if isinstance(tasks, list):
            return tasks
        return []
    except json.JSONDecodeError:
        return []


def generate_weekly_status_report(meeting_notes, api_key):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You write professional project status summaries."
            },
            {
                "role": "user",
                "content": SUMMARY_PROMPT + "\n" + meeting_notes
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()

from prompts import RISK_PROMPT


def analyze_project_risk(meeting_notes, api_key):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You analyze project delivery risks."
            },
            {
                "role": "user",
                "content": RISK_PROMPT + "\n" + meeting_notes
            }
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()

    try:
        risk = json.loads(content)
        return risk
    except:
        return {}