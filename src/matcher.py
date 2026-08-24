def calculate_match(resume_skills, job_skills):
    # Convert everything to lowercase
    resume_skills = {skill.lower().strip() for skill in resume_skills}
    job_skills = {skill.lower().strip() for skill in job_skills}

    # Skills present in both
    matched_skills = sorted(resume_skills.intersection(job_skills))

    # Skills required by job but missing from resume
    missing_skills = sorted(job_skills.difference(resume_skills))

    # Calculate score based on JOB requirements
    if not job_skills:
        score = 0
    else:
        score = round(
            (len(matched_skills) / len(job_skills)) * 100
        )

    return score, matched_skills, missing_skills