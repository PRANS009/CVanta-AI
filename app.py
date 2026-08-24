import os
import re

from flask import (
    Flask,
    jsonify,
    render_template,
    request
)

from werkzeug.utils import secure_filename


# =========================================================
# PROJECT MODULES
# =========================================================

from src.pdf_reader import extract_text_from_pdf

from src.skill_extractor import (
    extract_skills,
    detect_domain_locally,
    merge_skills
)

from src.ai_analyzer import (
    analyze_resume_with_ai,
    extract_resume_profile_with_ai,
    generate_professional_summary,
    generate_professional_headline,
    improve_project_description,
    improve_experience_description,
    recommend_skills,
    check_resume_readiness,
    generate_interview_questions,
    generate_learning_roadmap,
    detect_resume_gaps,
    check_resume_contradictions,
    verify_skill_evidence
)


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)


# =========================================================
# UPLOAD CONFIG
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MAX_CONTENT_LENGTH"] = (
    10 * 1024 * 1024
)

ALLOWED_EXTENSIONS = {
    "pdf"
}


# =========================================================
# HELPERS
# =========================================================

def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def get_json_data():

    return (
        request.get_json(
            silent=True
        )
        or
        {}
    )


# =========================================================
# CLEAN AI LIST ITEM
# =========================================================

def clean_ai_item(text):

    text = text.strip()

    text = re.sub(
        r"^[\-\•\*\✅\⚠️\🟡\🟢\🔴]+\s*",
        "",
        text
    )

    text = re.sub(
        r"^\d+[\.\)]\s*",
        "",
        text
    )

    return text.strip()


# =========================================================
# PARSE AI ANALYSIS INTO UI SECTIONS
# =========================================================

def parse_ai_result(ai_text):

    data = {

        "domain": "",

        "specialization": "",

        "best_role": "",

        "career_fit_score": 0,

        "career_fit_explanation": "",

        "alternative_roles": [],

        "skills": [],

        "tools": [],

        "strengths": [],

        "missing_skills": [],

        "improvements": [],

        "recommendation": ""
    }


    if not ai_text:

        return data


    lines = [
        line.strip()
        for line in ai_text.splitlines()
        if line.strip()
    ]


    current_section = None


    for line in lines:

        lower = line.lower()


        # =================================================
        # DETECT SECTION HEADINGS
        # =================================================

        if "detected domain" in lower:

            current_section = "domain"

            continue


        if "best matching job role" in lower:

            current_section = "best_role"

            continue


        if "career fit score" in lower:

            current_section = "career_fit"

            continue


        if "alternative job roles" in lower:

            current_section = "alternative_roles"

            continue


        if "detected skills" in lower:

            current_section = "skills"

            continue


        if (
            "tools / technologies / equipment"
            in lower
            or
            "tools / technologies" in lower
            or
            "tools / equipment" in lower
        ):

            current_section = "tools"

            continue


        if "resume strengths" in lower:

            current_section = "strengths"

            continue


        if (
            "missing / recommended skills"
            in lower
        ):

            current_section = "missing_skills"

            continue


        if (
            "resume improvements"
            in lower
            or
            "improvement suggestions"
            in lower
        ):

            current_section = "improvements"

            continue


        if (
            "career recommendation"
            in lower
        ):

            current_section = "recommendation"

            continue


        # =================================================
        # DOMAIN
        # =================================================

        if current_section == "domain":

            if lower.startswith("domain:"):

                data["domain"] = (
                    line.split(
                        ":",
                        1
                    )[1].strip()
                )

            elif lower.startswith(
                "specialization:"
            ):

                data["specialization"] = (
                    line.split(
                        ":",
                        1
                    )[1].strip()
                )

            elif not data["domain"]:

                data["domain"] = (
                    clean_ai_item(line)
                )

            elif not data["specialization"]:

                data["specialization"] = (
                    clean_ai_item(line)
                )


        # =================================================
        # BEST ROLE
        # =================================================

        elif current_section == "best_role":

            if not data["best_role"]:

                data["best_role"] = (
                    clean_ai_item(line)
                )


        # =================================================
        # CAREER FIT SCORE
        # =================================================

        elif current_section == "career_fit":

            score_match = re.search(
                r"(\d{1,3})\s*(?:/100|%)",
                line
            )


            if score_match:

                score = int(
                    score_match.group(1)
                )

                data["career_fit_score"] = (
                    max(
                        0,
                        min(
                            score,
                            100
                        )
                    )
                )

            else:

                cleaned = line

                if lower.startswith(
                    "explanation:"
                ):

                    cleaned = (
                        line.split(
                            ":",
                            1
                        )[1].strip()
                    )


                if cleaned:

                    if data[
                        "career_fit_explanation"
                    ]:

                        data[
                            "career_fit_explanation"
                        ] += " " + cleaned

                    else:

                        data[
                            "career_fit_explanation"
                        ] = cleaned


        # =================================================
        # ALTERNATIVE ROLES
        # =================================================

        elif (
            current_section
            ==
            "alternative_roles"
        ):

            item = clean_ai_item(
                line
            )

            if item:

                data[
                    "alternative_roles"
                ].append(item)


        # =================================================
        # SKILLS
        # =================================================

        elif current_section == "skills":

            item = clean_ai_item(
                line
            )

            if item:

                data[
                    "skills"
                ].append(item)


        # =================================================
        # TOOLS
        # =================================================

        elif current_section == "tools":

            item = clean_ai_item(
                line
            )

            if item:

                data[
                    "tools"
                ].append(item)


        # =================================================
        # STRENGTHS
        # =================================================

        elif current_section == "strengths":

            item = clean_ai_item(
                line
            )

            if item:

                data[
                    "strengths"
                ].append(item)


        # =================================================
        # MISSING SKILLS
        # =================================================

        elif (
            current_section
            ==
            "missing_skills"
        ):

            item = clean_ai_item(
                line
            )

            if item:

                data[
                    "missing_skills"
                ].append(item)


        # =================================================
        # IMPROVEMENTS
        # =================================================

        elif current_section == "improvements":

            item = clean_ai_item(
                line
            )

            if item:

                data[
                    "improvements"
                ].append(item)


        # =================================================
        # RECOMMENDATION
        # =================================================

        elif current_section == "recommendation":

            item = clean_ai_item(
                line
            )

            if item:

                if data["recommendation"]:

                    data[
                        "recommendation"
                    ] += " " + item

                else:

                    data[
                        "recommendation"
                    ] = item


    return data


# =========================================================
# HOME
# =========================================================

@app.route(
    "/",
    methods=["GET"]
)
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# RESUME BUILDER
# =========================================================

@app.route(
    "/resume-builder",
    methods=["GET"]
)
def resume_builder():

    return render_template(
        "resume_builder.html"
    )


# =========================================================
# MULTI-DOMAIN RESUME ANALYZER
# =========================================================

@app.route(
    "/upload",
    methods=["POST"]
)
def upload_resume():

    try:

        resume_file = (

            request.files.get(
                "resume"
            )

            or

            request.files.get(
                "file"
            )

            or

            request.files.get(
                "resume_file"
            )
        )


        if not resume_file:

            return (
                "No resume file uploaded.",
                400
            )


        if (
            resume_file.filename
            is None

            or

            resume_file.filename == ""
        ):

            return (
                "Please select a PDF resume.",
                400
            )


        if not allowed_file(
            resume_file.filename
        ):

            return (
                "Only PDF files are supported.",
                400
            )


        # =================================================
        # SAVE FILE
        # =================================================

        filename = secure_filename(
            resume_file.filename
        )


        file_path = os.path.join(

            app.config[
                "UPLOAD_FOLDER"
            ],

            filename
        )


        resume_file.save(
            file_path
        )


        # =================================================
        # EXTRACT PDF TEXT
        # =================================================

        resume_text = (

            extract_text_from_pdf(
                file_path
            )

            or

            ""
        )


        if not resume_text.strip():

            return (
                "Could not extract readable text from this PDF.",
                400
            )


        # =================================================
        # LOCAL SKILL DETECTION
        # =================================================

        local_skills = (
            extract_skills(
                resume_text
            )
        )


        local_domain = (
            detect_domain_locally(
                resume_text
            )
        )


        # =================================================
        # GEMINI MULTI-DOMAIN PROFILE
        # =================================================

        ai_profile = (
            extract_resume_profile_with_ai(

                resume_text,

                local_skills,

                local_domain
            )
        )


        ai_skills = (
            ai_profile.get(
                "skills",
                []
            )
        )


        ai_tools = (
            ai_profile.get(
                "tools",
                []
            )
        )


        # =================================================
        # MERGE SKILLS
        # =================================================

        final_skills = (
            merge_skills(

                local_skills,

                ai_skills
            )
        )


        final_skills = (
            merge_skills(

                final_skills,

                ai_tools
            )
        )


        detected_domain = (

            ai_profile.get(
                "domain"
            )

            or

            local_domain

            or

            "General / Multidisciplinary"
        )


        specialization = (
            ai_profile.get(
                "specialization",
                ""
            )
        )


        best_roles = (
            ai_profile.get(
                "best_roles",
                []
            )
        )


        # =================================================
        # UPDATE PROFILE
        # =================================================

        ai_profile["skills"] = (
            final_skills
        )


        ai_profile["domain"] = (
            detected_domain
        )


        # =================================================
        # AI CAREER ANALYSIS
        # =================================================

        ai_analysis = (
            analyze_resume_with_ai(

                resume_text,

                ai_profile
            )
        )


        # =================================================
        # PARSE AI RESULT
        # =================================================

        parsed_result = (
            parse_ai_result(
                ai_analysis
            )
        )


        # =================================================
        # FALLBACK VALUES
        # =================================================

        if not parsed_result[
            "domain"
        ]:

            parsed_result[
                "domain"
            ] = detected_domain


        if not parsed_result[
            "specialization"
        ]:

            parsed_result[
                "specialization"
            ] = specialization


        if (
            not parsed_result[
                "best_role"
            ]

            and

            best_roles
        ):

            parsed_result[
                "best_role"
            ] = best_roles[0]


        if (
            not parsed_result[
                "alternative_roles"
            ]

            and

            len(best_roles) > 1
        ):

            parsed_result[
                "alternative_roles"
            ] = best_roles[1:]


        if not parsed_result[
            "skills"
        ]:

            parsed_result[
                "skills"
            ] = final_skills


        if not parsed_result[
            "tools"
        ]:

            parsed_result[
                "tools"
            ] = ai_tools


        # =================================================
        # RESULT PAGE
        # =================================================

        return render_template(

            "result.html",

            filename=filename,

            skills=final_skills,

            extracted_skills=final_skills,

            detected_domain=detected_domain,

            domain=detected_domain,

            specialization=specialization,

            best_roles=best_roles,

            tools=ai_tools,

            profile=ai_profile,

            ai_analysis=ai_analysis,

            analysis=ai_analysis,

            result=ai_analysis,

            parsed_result=parsed_result
        )


    except Exception as error:

        print(
            "Resume upload error:",
            error
        )


        return (
            "Something went wrong while analyzing the resume. "
            "Please try again.",
            500
        )


# =========================================================
# DETECT BUILDER PROFILE DOMAIN
# =========================================================

@app.route(
    "/detect-profile-domain",
    methods=["POST"]
)
def detect_profile_domain():

    try:

        data = get_json_data()


        profile_text = f"""
Skills:
{data.get("skills", "")}

Education:
{data.get("education", "")}

Experience:
{data.get("experience", "")}

Projects:
{data.get("project", "")}

Certifications:
{data.get("certifications", "")}
"""


        local_skills = (
            extract_skills(
                profile_text
            )
        )


        local_domain = (
            detect_domain_locally(
                profile_text
            )
        )


        ai_profile = (
            extract_resume_profile_with_ai(

                profile_text,

                local_skills,

                local_domain
            )
        )


        final_skills = (
            merge_skills(

                local_skills,

                ai_profile.get(
                    "skills",
                    []
                )
            )
        )


        return jsonify({

            "domain":
                ai_profile.get(
                    "domain",
                    local_domain
                ),

            "specialization":
                ai_profile.get(
                    "specialization",
                    ""
                ),

            "skills":
                final_skills,

            "tools":
                ai_profile.get(
                    "tools",
                    []
                ),

            "best_roles":
                ai_profile.get(
                    "best_roles",
                    []
                )
        })


    except Exception as error:

        print(
            "Domain detection error:",
            error
        )


        return jsonify({
            "error":
                "Could not detect profile domain."
        }), 500


# =========================================================
# GENERATE SUMMARY
# =========================================================

@app.route(
    "/generate-summary",
    methods=["POST"]
)
def generate_summary():

    try:

        data = get_json_data()


        summary = (
            generate_professional_summary(

                data.get(
                    "name",
                    ""
                ),

                data.get(
                    "skills",
                    ""
                ),

                data.get(
                    "education",
                    ""
                ),

                data.get(
                    "experience",
                    ""
                ),

                data.get(
                    "project",
                    ""
                )
            )
        )


        return jsonify({
            "summary":
                summary
        })


    except Exception as error:

        print(
            "Summary error:",
            error
        )


        return jsonify({
            "error":
                "Could not generate summary."
        }), 500


# =========================================================
# HEADLINE
# =========================================================

@app.route(
    "/generate-headline",
    methods=["POST"]
)
def generate_headline():

    try:

        data = get_json_data()


        headline = (
            generate_professional_headline(

                data.get(
                    "skills",
                    ""
                ),

                data.get(
                    "education",
                    ""
                ),

                data.get(
                    "experience",
                    ""
                ),

                data.get(
                    "project",
                    ""
                )
            )
        )


        return jsonify({
            "headline":
                headline
        })


    except Exception as error:

        print(
            "Headline error:",
            error
        )


        return jsonify({
            "error":
                "Could not generate headline."
        }), 500


# =========================================================
# IMPROVE PROJECT
# =========================================================

@app.route(
    "/improve-project",
    methods=["POST"]
)
def improve_project():

    try:

        data = get_json_data()


        project_name = (
            data.get(
                "project_name",
                ""
            )
        )


        project_description = (
            data.get(
                "project_description",
                ""
            )
        )


        if (
            not project_name.strip()

            or

            not project_description.strip()
        ):

            return jsonify({
                "error":
                    "Project name and description are required."
            }), 400


        improved = (
            improve_project_description(

                project_name,

                project_description
            )
        )


        return jsonify({
            "improved_description":
                improved
        })


    except Exception as error:

        print(
            "Project improve error:",
            error
        )


        return jsonify({
            "error":
                "Could not improve project."
        }), 500


# =========================================================
# IMPROVE EXPERIENCE
# =========================================================

@app.route(
    "/improve-experience",
    methods=["POST"]
)
def improve_experience():

    try:

        data = get_json_data()


        title = (
            data.get(
                "job_title",
                ""
            )
        )


        company = (
            data.get(
                "company",
                ""
            )
        )


        description = (
            data.get(
                "experience_description",
                ""
            )
        )


        if (
            not title.strip()

            or

            not description.strip()
        ):

            return jsonify({
                "error":
                    "Job title and description are required."
            }), 400


        improved = (
            improve_experience_description(

                title,

                company,

                description
            )
        )


        return jsonify({
            "improved_description":
                improved
        })


    except Exception as error:

        print(
            "Experience improve error:",
            error
        )


        return jsonify({
            "error":
                "Could not improve experience."
        }), 500


# =========================================================
# SKILL RECOMMENDATIONS
# =========================================================

@app.route(
    "/recommend-skills",
    methods=["POST"]
)
def recommend_resume_skills():

    try:

        data = get_json_data()


        recommendations = (
            recommend_skills(

                data.get(
                    "current_skills",
                    ""
                ),

                data.get(
                    "education",
                    ""
                ),

                data.get(
                    "experience",
                    ""
                ),

                data.get(
                    "project",
                    ""
                )
            )
        )


        return jsonify({
            "recommendations":
                recommendations
        })


    except Exception as error:

        print(
            "Skill recommendation error:",
            error
        )


        return jsonify({
            "error":
                "Could not recommend skills."
        }), 500


# =========================================================
# READINESS
# =========================================================

@app.route(
    "/check-readiness",
    methods=["POST"]
)
def check_readiness():

    try:

        data = get_json_data()


        result = (
            check_resume_readiness(

                data.get(
                    "summary",
                    ""
                ),

                data.get(
                    "skills",
                    ""
                ),

                data.get(
                    "education",
                    ""
                ),

                data.get(
                    "experience",
                    ""
                ),

                data.get(
                    "project",
                    ""
                ),

                data.get(
                    "certifications",
                    ""
                )
            )
        )


        return jsonify({
            "readiness_result":
                result
        })


    except Exception as error:

        print(
            "Readiness error:",
            error
        )


        return jsonify({
            "error":
                "Could not check readiness."
        }), 500


# =========================================================
# INTERVIEW QUESTIONS
# =========================================================

@app.route(
    "/generate-interview-questions",
    methods=["POST"]
)
def interview_questions():

    try:

        data = get_json_data()


        result = (
            generate_interview_questions(

                data.get(
                    "skills",
                    ""
                ),

                data.get(
                    "experience",
                    ""
                ),

                data.get(
                    "project",
                    ""
                ),

                data.get(
                    "education",
                    ""
                )
            )
        )


        return jsonify({
            "questions":
                result
        })


    except Exception as error:

        print(
            "Interview error:",
            error
        )


        return jsonify({
            "error":
                "Could not generate interview questions."
        }), 500


# =========================================================
# ROADMAP
# =========================================================

@app.route(
    "/generate-roadmap",
    methods=["POST"]
)
def roadmap():

    try:

        data = get_json_data()


        result = (
            generate_learning_roadmap(

                data.get(
                    "skills",
                    ""
                ),

                data.get(
                    "education",
                    ""
                ),

                data.get(
                    "experience",
                    ""
                ),

                data.get(
                    "project",
                    ""
                )
            )
        )


        return jsonify({
            "roadmap":
                result
        })


    except Exception as error:

        print(
            "Roadmap error:",
            error
        )


        return jsonify({
            "error":
                "Could not generate roadmap."
        }), 500


# =========================================================
# RESUME GAP DETECTOR
# =========================================================

@app.route(
    "/detect-resume-gaps",
    methods=["POST"]
)
def resume_gaps():

    try:

        data = get_json_data()


        result = (
            detect_resume_gaps(

                data.get(
                    "summary",
                    ""
                ),

                data.get(
                    "skills",
                    ""
                ),

                data.get(
                    "education",
                    ""
                ),

                data.get(
                    "experience",
                    ""
                ),

                data.get(
                    "project",
                    ""
                ),

                data.get(
                    "certifications",
                    ""
                )
            )
        )


        return jsonify({
            "gap_result":
                result
        })


    except Exception as error:

        print(
            "Gap detector error:",
            error
        )


        return jsonify({
            "error":
                "Could not detect gaps."
        }), 500


# =========================================================
# CONSISTENCY
# =========================================================

@app.route(
    "/check-contradictions",
    methods=["POST"]
)
def contradictions():

    try:

        data = get_json_data()


        result = (
            check_resume_contradictions(

                data.get(
                    "skills",
                    ""
                ),

                data.get(
                    "education",
                    ""
                ),

                data.get(
                    "experience",
                    ""
                ),

                data.get(
                    "project",
                    ""
                ),

                data.get(
                    "certifications",
                    ""
                )
            )
        )


        return jsonify({
            "contradiction_result":
                result
        })


    except Exception as error:

        print(
            "Consistency error:",
            error
        )


        return jsonify({
            "error":
                "Could not check consistency."
        }), 500


# =========================================================
# SKILL EVIDENCE
# =========================================================

@app.route(
    "/verify-skills",
    methods=["POST"]
)
def verify_skills():

    try:

        data = get_json_data()


        skills = (
            data.get(
                "skills",
                ""
            )
        )


        if not skills.strip():

            return jsonify({
                "error":
                    "Please enter skills first."
            }), 400


        result = (
            verify_skill_evidence(

                skills,

                data.get(
                    "education",
                    ""
                ),

                data.get(
                    "experience",
                    ""
                ),

                data.get(
                    "project",
                    ""
                )
            )
        )


        return jsonify({
            "skill_evidence_result":
                result
        })


    except Exception as error:

        print(
            "Skill evidence error:",
            error
        )


        return jsonify({
            "error":
                "Could not verify skills."
        }), 500


# =========================================================
# ERRORS
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    return (
        "Page not found.",
        404
    )


@app.errorhandler(413)
def file_too_large(error):

    return (
        "PDF is too large. Maximum size is 10 MB.",
        413
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5001
    )