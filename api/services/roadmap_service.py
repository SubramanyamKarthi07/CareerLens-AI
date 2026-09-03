from api.ai.roadmap_generator import generate_learning_roadmap
from api.services.matching_service import match_resume_with_jobs
from api.services.skill_service import get_resume_skills
from api.ai.career_progression import recommend_next_skills

def get_learning_roadmap(missing_skills):
    """
    Generate a learning roadmap based on missing skills.
    """
    return generate_learning_roadmap(missing_skills)




def generate_roadmap_from_resume(db, resume_text):
    """
    Generate a personalized learning roadmap from a resume.
    """

    # Extract resume skills
    resume_skills = get_resume_skills(resume_text)

    # Get next recommended skills
    next_skills = recommend_next_skills(resume_skills)

    # If no next skills, return advanced roadmap
    if not next_skills:
        return generate_learning_roadmap([])

    # Generate roadmap
    return generate_learning_roadmap(next_skills)