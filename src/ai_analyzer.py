import os
import json

from dotenv import load_dotenv
from google import genai

from src.skill_extractor import detect_domain_locally


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")


if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please add GEMINI_API_KEY to your .env file."
    )


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=API_KEY
)


MODEL_NAME = "gemini-3.6-flash"


# =========================================================
# COMMON AI FUNCTION
# =========================================================

def _generate_ai_response(
    prompt,
    fallback_message="AI response could not be generated."
):

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if not response or not response.text:

            return fallback_message

        return response.text.strip()

    except Exception as error:

        print(
            "Gemini API Error:",
            error
        )

        return fallback_message


# =========================================================
# JSON / DOMAIN HELPERS
# =========================================================

def _parse_ai_json(text):
    if not text:
        return {}

    cleaned = (
        str(text)
        .strip()
        .replace("```json", "")
        .replace("```JSON", "")
        .replace("```", "")
        .strip()
    )

    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")

    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        cleaned = cleaned[first_brace:last_brace + 1]

    try:
        data = json.loads(cleaned)
        return data if isinstance(data, dict) else {}
    except Exception as error:
        print("AI JSON parse error:", error)
        return {}


def _domain_hint(*parts):
    combined_text = " ".join(str(part or "") for part in parts)

    try:
        return detect_domain_locally(combined_text)
    except Exception as error:
        print("Local domain detection error:", error)
        return "General / Multidisciplinary"


def _safe_list(value):
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]

    if isinstance(value, str) and value.strip():
        return [item.strip() for item in value.split(",") if item.strip()]

    return []


# =========================================================
# MULTI-DOMAIN PROFILE EXTRACTION
# =========================================================

def extract_resume_profile_with_ai(
    resume_text,
    local_skills=None,
    local_domain=""
):
    if local_skills is None:
        local_skills = []

    if not resume_text or not resume_text.strip():
        return {
            "domain": local_domain or "General / Multidisciplinary",
            "specialization": "",
            "skills": list(local_skills),
            "tools": [],
            "certifications": [],
            "best_roles": []
        }

    prompt = f"""
You are a multi-domain resume information extraction system.

The candidate may belong to ANY profession, industry, engineering branch,
academic field, business function, healthcare area, creative field,
vocational trade, technician role or skilled occupation.

Examples include Computer Science, IT, AI/ML, Mechanical, Civil, Electrical,
Electronics, Automobile, Aerospace, Marine, Chemical, Biotechnology, Pharmacy,
Healthcare, Nursing, Architecture, Agriculture, Manufacturing, Finance,
Commerce, Accounting, Marketing, Sales, HR, Supply Chain, Management, Law,
Teaching, Hospitality, Design, UI/UX, ITI and technical trades.

LOCAL DOMAIN HINT:
{local_domain}

LOCALLY DETECTED SKILLS:
{local_skills}

RESUME:
------------------------
{resume_text[:50000]}
------------------------

Analyze the resume without assuming it belongs to software or IT.
Extract only information actually stated or clearly demonstrated.
Do not invent skills, tools, qualifications, certifications, experience or achievements.

Return ONLY valid JSON using exactly this schema:

{{
    "domain": "main professional domain",
    "specialization": "specific specialization or empty string",
    "skills": ["skill 1", "skill 2"],
    "tools": ["tool or equipment 1"],
    "certifications": ["certification 1"],
    "best_roles": ["role 1", "role 2", "role 3"]
}}
"""

    raw_response = _generate_ai_response(prompt, "{}")
    profile = _parse_ai_json(raw_response)

    if not profile:
        profile = {}

    profile["domain"] = (
        str(profile.get("domain", "")).strip()
        or local_domain
        or "General / Multidisciplinary"
    )
    profile["specialization"] = str(profile.get("specialization", "")).strip()
    profile["skills"] = _safe_list(profile.get("skills")) or list(local_skills)
    profile["tools"] = _safe_list(profile.get("tools"))
    profile["certifications"] = _safe_list(profile.get("certifications"))
    profile["best_roles"] = _safe_list(profile.get("best_roles"))[:5]

    return profile


# =========================================================
# 1. COMPLETE RESUME ANALYZER
# =========================================================

def analyze_resume_with_ai(
    resume_text,
    profile=None
):
    if not resume_text or not resume_text.strip():
        return (
            "Resume text could not be extracted. "
            "Please upload a readable PDF resume."
        )

    resume_text = resume_text[:50000]

    if not isinstance(profile, dict):
        profile = {}

    domain = profile.get("domain", "")
    specialization = profile.get("specialization", "")
    skills = profile.get("skills", [])
    tools = profile.get("tools", [])
    best_roles = profile.get("best_roles", [])

    prompt = f"""
You are an expert multi-domain recruiter, ATS reviewer and career advisor.

Evaluate resumes from ANY profession or trade.
Never assume the candidate belongs to software or IT.

DETECTED DOMAIN:
{domain}

SPECIALIZATION:
{specialization}

DETECTED SKILLS:
{skills}

TOOLS / SOFTWARE / MACHINES / EQUIPMENT:
{tools}

POTENTIAL ROLES:
{best_roles}

RESUME:
----------------------------
{resume_text}
----------------------------

IMPORTANT RULES:
- Use only information supported by the resume.
- Never invent qualifications, skills, companies, experience, certifications,
  licenses, tools or achievements.
- Adapt the analysis to the candidate's actual profession.
- Missing skills must be clearly marked as recommendations.
- Students and freshers should not be penalized merely because they have no
  full-time work experience.
- Do not use markdown tables.

Return exactly this structure:

🏷️ DETECTED DOMAIN
State the professional domain and specialization when clear.

🎯 BEST MATCHING JOB ROLE
Give the strongest realistic role.

📊 CAREER FIT SCORE
Give a score out of 100 and explain briefly.

💼 ALTERNATIVE JOB ROLES
Give 3 realistic alternative roles.

🧠 DETECTED SKILLS
List important skills actually visible in the resume.

🛠 TOOLS / TECHNOLOGIES / EQUIPMENT
List tools, software, platforms, machines or equipment actually supported by the resume.

💪 RESUME STRENGTHS
List the strongest parts of the resume.

⚠️ MISSING / RECOMMENDED SKILLS
Recommend useful skills for this candidate's actual field and clearly mark them as recommendations.

🔧 RESUME IMPROVEMENTS
Give specific, practical improvements.

🚀 CAREER RECOMMENDATION
Give a short practical next step.
"""

    return _generate_ai_response(
        prompt,
        "AI analysis is temporarily unavailable. Please try again."
    )


# =========================================================
# 2. PROFESSIONAL SUMMARY GENERATOR
# =========================================================

def generate_professional_summary(
    name,
    skills,
    education,
    experience,
    project
):

    prompt = f"""
You are an expert professional resume writer for candidates from ANY industry, profession or trade.

Write a strong professional summary for this candidate.

NAME:
{name}

SKILLS:
{skills}

EDUCATION:
{education}

EXPERIENCE:
{experience}

PROJECTS:
{project}

RULES:

- Use only the information provided.
- Never invent experience, achievements, skills or qualifications.
- Write 2 to 4 sentences.
- Keep the summary around 45 to 80 words.
- Make it ATS-friendly.
- Keep it suitable for internships, fresher roles or early-career jobs.
- Avoid generic phrases such as:
  "hardworking",
  "passionate",
  "highly motivated",
  "dynamic individual".
- Do not use bullet points.
- Do not add a heading.
- Return only the professional summary.
"""


    return _generate_ai_response(
        prompt,
        (
            "Professional summary could not be generated. "
            "Please try again."
        )
    )


# =========================================================
# 3. PROFESSIONAL HEADLINE GENERATOR
# =========================================================

def generate_professional_headline(
    skills,
    education,
    experience,
    project
):

    prompt = f"""
You are an expert multi-domain resume writer.

Create ONE short professional resume headline
based only on the candidate information below.

SKILLS:
{skills}

EDUCATION:
{education}

EXPERIENCE:
{experience}

PROJECTS:
{project}

RULES:

- Use only information that is supported by the candidate data.
- Never invent skills, experience or job titles.
- Keep the headline between 5 and 14 words.
- Make the strongest realistic career direction clear.
- Important technical skills may be included.
- Use the | symbol to separate major parts when appropriate.
- Do not use quotation marks.
- Do not use a full sentence.
- Do not add explanation.
- Return ONLY the headline.

Example style:

AI/ML Developer | Python | Flask | Machine Learning
"""


    return _generate_ai_response(
        prompt,
        "Technology Candidate"
    )


# =========================================================
# 4. PROJECT DESCRIPTION IMPROVER
# =========================================================

def improve_project_description(
    project_name,
    project_description
):

    prompt = f"""
You are an expert multi-domain resume writer.

Improve the following project description for a professional resume.

PROJECT NAME:
{project_name}

CURRENT DESCRIPTION:
{project_description}

RULES:

- Preserve the candidate's original facts.
- Do not invent technologies, results, users, metrics,
  features or achievements.
- Make the wording stronger and professional.
- Highlight what was built and the candidate's contribution.
- Mention technologies only if they are already present.
- Keep it concise.
- Prefer 2 to 4 strong resume-style sentences.
- Do not add a heading.
- Return only the improved description.
"""


    return _generate_ai_response(
        prompt,
        project_description
    )


# =========================================================
# 5. EXPERIENCE DESCRIPTION IMPROVER
# =========================================================

def improve_experience_description(
    job_title,
    company,
    experience_description
):

    prompt = f"""
You are an expert professional resume writer for candidates from ANY industry, profession or trade.

Improve the following work or internship experience description.

JOB TITLE:
{job_title}

COMPANY:
{company}

CURRENT DESCRIPTION:
{experience_description}

RULES:

- Preserve all original facts.
- Do not invent responsibilities, numbers, technologies,
  achievements or results.
- Use strong professional action-oriented language.
- Highlight contribution and responsibilities.
- Make the description ATS-friendly.
- Keep it concise.
- Prefer 2 to 4 strong sentences.
- Return only the improved experience description.
"""


    return _generate_ai_response(
        prompt,
        experience_description
    )


# =========================================================
# 6. AI SKILL RECOMMENDATION
# =========================================================

def recommend_skills(
    current_skills,
    education,
    experience,
    project
):

    prompt = f"""
You are a career advisor and recruiter covering ALL industries, professions and technical trades.

Analyze this candidate profile.

CURRENT SKILLS:
{current_skills}

EDUCATION:
{education}

EXPERIENCE:
{experience}

PROJECTS:
{project}

Recommend useful additional skills that could strengthen
the candidate's resume and career opportunities.

IMPORTANT:

- Recommended skills are NOT existing candidate skills.
- Do not claim that the candidate already knows them.
- Avoid recommending skills that are already clearly present.
- Recommend realistic skills connected to the candidate's profile.
- Focus on practical employability.

Return:

🎯 Recommended Skills

1. Skill — short reason
2. Skill — short reason
3. Skill — short reason
4. Skill — short reason
5. Skill — short reason

Finish with:

📌 Priority:
Mention the top 2 skills the candidate should consider learning first.
"""


    return _generate_ai_response(
        prompt,
        (
            "Skill recommendations could not "
            "be generated right now."
        )
    )


# =========================================================
# 7. RESUME READINESS CHECKER
# =========================================================

def check_resume_readiness(
    summary,
    skills,
    education,
    experience,
    project,
    certifications
):

    prompt = f"""
You are an expert ATS resume reviewer covering ALL industries, professions and technical trades.

Evaluate this resume profile.

PROFESSIONAL SUMMARY:
{summary}

SKILLS:
{skills}

EDUCATION:
{education}

EXPERIENCE:
{experience}

PROJECTS:
{project}

CERTIFICATIONS:
{certifications}

Evaluate the resume based on:

- completeness
- clarity
- skills
- education
- projects
- experience
- ATS readability
- evidence supporting the candidate's abilities

IMPORTANT RULES:

- Missing sections should reduce the score only when they are
  genuinely useful for this candidate.
- Students and freshers may not have professional experience.
- Do not invent resume information.

Return exactly:

📊 RESUME READINESS SCORE
XX / 100

✅ STRONG AREAS
• ...
• ...
• ...

⚠️ NEEDS IMPROVEMENT
• ...
• ...
• ...

🎯 TOP 3 ACTIONS
1. ...
2. ...
3. ...

🏁 VERDICT
One short overall verdict.
"""


    return _generate_ai_response(
        prompt,
        (
            "Resume readiness could not "
            "be checked right now."
        )
    )


# =========================================================
# 8. INTERVIEW QUESTION GENERATOR
# =========================================================

def generate_interview_questions(
    skills,
    experience,
    project,
    education
):

    prompt = f"""
You are an expert interviewer covering ALL industries, professions and technical trades.

Create personalized interview questions for this candidate.

SKILLS:
{skills}

EXPERIENCE:
{experience}

PROJECTS:
{project}

EDUCATION:
{education}

RULES:

- Use only the candidate's provided information.
- Do not invent skills or experience.
- Questions should be suitable for internships,
  fresher jobs and early-career positions.
- Include technical questions.
- Include project-based questions when projects exist.
- Include experience questions when experience exists.
- Include 2 behavioral questions.
- Generate exactly 10 questions.
- Do NOT provide answers.
- Return only a numbered list.

Format:

1. Question
2. Question
3. Question
...
10. Question
"""


    return _generate_ai_response(
        prompt,
        (
            "Interview questions could not "
            "be generated right now."
        )
    )


# =========================================================
# 9. CAREER LEARNING ROADMAP
# =========================================================

def generate_learning_roadmap(
    skills,
    education,
    experience,
    project
):

    prompt = f"""
You are an expert career mentor covering ALL industries, professions and technical trades.

Create a realistic learning roadmap for this candidate.

CURRENT SKILLS:
{skills}

EDUCATION:
{education}

EXPERIENCE:
{experience}

PROJECTS:
{project}

RULES:

- Base the roadmap on the candidate's current profile.
- Do not claim that recommended skills are already known.
- Focus on practical learning.
- Avoid unrealistic expectations.
- Make the roadmap suitable for a student,
  fresher or early-career candidate.

Return:

🎯 RECOMMENDED CAREER DIRECTION
One realistic career direction.

📍 CURRENT LEVEL
Brief assessment.

1️⃣ PHASE 1 — FOUNDATION
What to strengthen first.

2️⃣ PHASE 2 — CORE SKILLS
Important technical skills.

3️⃣ PHASE 3 — PROJECTS
What types of projects should be built.

4️⃣ PHASE 4 — INDUSTRY READINESS
GitHub, resume, interview and practical preparation.

5️⃣ PHASE 5 — JOB PREPARATION
How to prepare for internships or entry-level roles.

🏁 FINAL TARGET
A short realistic goal.
"""


    return _generate_ai_response(
        prompt,
        (
            "Career roadmap could not "
            "be generated right now."
        )
    )


# =========================================================
# 10. RESUME GAP DETECTOR
# =========================================================

def detect_resume_gaps(
    summary,
    skills,
    education,
    experience,
    project,
    certifications
):

    prompt = f"""
You are an expert multi-domain resume reviewer.

Analyze the following resume data and identify important
missing or weak areas.

SUMMARY:
{summary}

SKILLS:
{skills}

EDUCATION:
{education}

EXPERIENCE:
{experience}

PROJECTS:
{project}

CERTIFICATIONS:
{certifications}

IMPORTANT RULES:

- Do not invent missing facts.
- Do not criticize someone simply for being a fresher.
- Experience is not mandatory for a student resume.
- Identify genuine weaknesses and opportunities to improve.
- Separate missing information from optional recommendations.

Return:

🔎 RESUME GAP ANALYSIS

🔴 IMPORTANT GAPS
• ...

🟡 WEAK / UNCLEAR AREAS
• ...

🟢 OPTIONAL IMPROVEMENTS
• ...

🎯 HIGHEST PRIORITY FIX
Give one most important improvement.
"""


    return _generate_ai_response(
        prompt,
        (
            "Resume gap analysis could not "
            "be generated right now."
        )
    )


# =========================================================
# 11. CONTRADICTION / CONSISTENCY CHECK
# =========================================================

def check_resume_contradictions(
    skills,
    education,
    experience,
    project,
    certifications
):

    prompt = f"""
You are an expert multi-domain resume quality reviewer.

Check this resume for contradictions, inconsistencies
or suspicious mismatches.

SKILLS:
{skills}

EDUCATION:
{education}

EXPERIENCE:
{experience}

PROJECTS:
{project}

CERTIFICATIONS:
{certifications}

Examples of issues:

- A skill claimed without any supporting evidence.
- Technology mentioned in one section but contradicted elsewhere.
- Dates or qualifications that appear inconsistent.
- Project claims that conflict with the skills section.

IMPORTANT:

- Do not assume something is false merely because evidence
  is not available.
- Distinguish between contradiction and missing evidence.
- Do not invent issues.

Return:

⚠️ RESUME CONSISTENCY CHECK

STATUS:
Choose one:
GOOD
NEEDS REVIEW
ISSUES FOUND

🔍 FINDINGS
• ...

✅ CONSISTENT AREAS
• ...

🛠 RECOMMENDATIONS
• ...
"""


    return _generate_ai_response(
        prompt,
        (
            "Resume consistency could not "
            "be checked right now."
        )
    )


# =========================================================
# 12. SKILL EVIDENCE CHECK
# =========================================================

def verify_skill_evidence(
    skills,
    education,
    experience,
    project
):

    prompt = f"""
You are an expert multi-domain resume reviewer.

Check whether the skills claimed by this candidate are supported
by their education, projects or experience.

CLAIMED SKILLS:
{skills}

EDUCATION:
{education}

EXPERIENCE:
{experience}

PROJECTS:
{project}

IMPORTANT RULES:

- Do not assume the candidate does not know a skill merely because
  evidence is missing from the resume.
- Classify it as "Needs More Evidence" instead.
- Use only the supplied resume data.
- Do not invent projects or experience.

For important skills, classify them as:

✅ Strong Evidence
The resume clearly demonstrates the skill.

🟡 Some Evidence
The resume partially supports the skill.

⚠️ Needs More Evidence
The skill is listed but not demonstrated clearly.

Return:

🧠 SKILL EVIDENCE REPORT

✅ STRONG EVIDENCE
• Skill — evidence

🟡 SOME EVIDENCE
• Skill — evidence

⚠️ NEEDS MORE EVIDENCE
• Skill — explanation

🎯 RECOMMENDATION
Explain how the candidate can demonstrate weaker skills
through real projects, education or experience.
"""


    return _generate_ai_response(
        prompt,
        (
            "Skill evidence could not "
            "be checked right now."
        )
    )