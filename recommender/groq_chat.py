import os
from openai import OpenAI


def ask_groq(message, profile, result):
    api_key = os.environ.get("GROQ_API_KEY")
    model = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")

    if not api_key:
        return "Groq API key is missing. Add GROQ_API_KEY in the .env file."

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )

    context = build_context(profile, result)

    try:
        response = client.responses.create(
            model=model,
            input=context + "\n\nStudent question: " + message
        )
        return clean_output(response.output_text)
    except Exception as error:
        return "Chat service error: " + str(error)


def build_context(profile, result):
    best = result.get("best", {})
    careers = result.get("careers", [])
    career_names = ", ".join([career.get("career", "") for career in careers])

    return """
You are a helpful AI career advisor inside a 4th semester Programming for AI Flask project.
Write clean plain text only. Do not use Markdown or tables.
Avoid headings with #, avoid bullet characters like -, *, •, and avoid emoji.
Use short paragraphs and numbered steps like 1) 2) 3) when needed.

Student profile:
Name: {name}
Marks: {marks}
Interests: {interests}
Skills: {skills}
Preferred work: {preferred_work}
Math level: {math_level}
Goal: {goal}

Current recommendation:
Degree: {degree}
Score: {score}
Careers: {careers}

Answer briefly and guide the student toward useful next steps.
""".format(
        name=profile.get("name", "Student"),
        marks=profile.get("marks", ""),
        interests=", ".join(profile.get("interests", [])),
        skills=", ".join(profile.get("skills", [])),
        preferred_work=profile.get("preferred_work", ""),
        math_level=profile.get("math_level", ""),
        goal=profile.get("goal", ""),
        degree=best.get("degree", "Not calculated yet"),
        score=best.get("score", ""),
        careers=career_names
    )


def clean_output(text):
    if not text:
        return ""

    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    cleaned = []

    for raw in lines:
        line = raw.strip()
        if not line:
            cleaned.append("")
            continue

        if line.startswith("```") or line.startswith("|") or set(line) == {"-"}:
            continue

        if line.startswith("#"):
            line = line.lstrip("#").strip()

        if line.startswith(("-", "*", "•")):
            line = line[1:].strip()

        line = line.replace("**", "").replace("__", "").replace("`", "")
        cleaned.append(line)

    out_lines = []
    blank = False
    for line in cleaned:
        if line == "":
            if not blank:
                out_lines.append("")
            blank = True
        else:
            out_lines.append(line)
            blank = False

    return "\n".join(out_lines).strip()
