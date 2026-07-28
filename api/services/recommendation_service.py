from api.repositories.recommendation_repository import recommend_jobs


def job_recommendation(db, skills):
    return recommend_jobs(db, skills)