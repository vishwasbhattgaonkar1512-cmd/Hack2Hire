def extract_skills(resume_text):
    skills_db = [
        "python", "java", "flask", "html", "css", "javascript",
        "machine learning", "sql", "data structures",
        "marketing", "finance", "biology", "anatomy"
    ]
    resume = resume_text.lower()
    return [s for s in skills_db if s in resume]
