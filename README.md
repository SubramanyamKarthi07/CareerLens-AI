# CareerLens-AI
### AI-Powered Career Intelligence and Skill-Gap Analysis Platform

## 1. Project Overview

CareerLens-AI is a career intelligence platform that analyzes a user's resume, evaluates relevant skills, recommends matching job opportunities, identifies potential skill gaps, and generates a personalized learning roadmap.

The project combines resume analysis, job matching, and career guidance to help users make informed decisions about their career development.

## 2. Key Features

- **Resume Analysis:** Evaluates resume quality based on skills, projects, experience, education, certifications, and content structure.
- **Skill Extraction:** Identifies relevant technical and analytical skills from resume text.
- **Job Recommendations:** Matches resume skills against job descriptions and ranks relevant opportunities.
- **Role and Location Relevance:** Adjusts job rankings based on career-role relevance and preferred locations.
- **Skill-Gap Analysis:** Highlights skills identified as missing from recommended job requirements.
- **Career Summary:** Generates a career-level classification and summarizes strengths and improvement areas.
- **Learning Roadmap:** Creates a four-week learning plan with goals and practical exercises.

## 3. Technology Stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **ORM and SQL Access:** SQLAlchemy
- **Data Analysis:** Pandas, NumPy
- **Validation:** Pydantic
- **API Documentation:** Swagger UI

## 4. Project Architecture

The application separates responsibilities into API routes, schemas, repositories, services, and AI-assisted analysis modules.

- `api/` — API endpoints, schemas, business services, and analysis modules.
- `config/` — Application and database configuration.
- `database/` — Database connection utilities and scripts.
- `etl/` — Data extraction, transformation, and loading workflows.
- `analytics/` — Data exploration and analytics scripts.
- `data/` — Project datasets.
- `docs/` — Project documentation.
- `tests/` — Reserved for automated tests.

## 5. Prerequisites

- Python installed
- PostgreSQL installed and running
- Git
- A terminal such as PowerShell

## 6. Installation and Setup

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd CareerLens-AI
```

Create and activate a virtual environment on Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Configure the database connection using the project's existing configuration. Set the required database credentials in your local environment configuration.

**Security:** Never publish database passwords, API keys, or other secrets.

Ensure PostgreSQL is running and the required database and tables have been created.

## 7. Run the Application

From the project root, activate the virtual environment and run:

```powershell
python -m uvicorn api.main:app --reload
```

Open the API documentation:

http://127.0.0.1:8000/docs

Use the available endpoints to explore the API. The career report endpoint accepts resume text according to its request schema.

## 8. Career Report Output

The career report can include:

- Resume quality score
- Professional strengths
- Improvement areas and potential skill gaps
- Ranked job recommendations
- Matched and missing skills
- Technical match scores
- Career-level classification
- Career summary
- Four-week learning roadmap

## 9. Database

CareerLens-AI uses PostgreSQL to store job-related data and support job matching and analytics. Database connectivity can be checked using:

```powershell
python -m database.scripts.test_connection
```

## 10. Current Limitations

- Resume scoring uses rule-based checks and should be treated as an indicative score, not a guaranteed measure of resume quality.
- Skill-gap detection depends on the skills extracted from available job descriptions.
- Job recommendations depend on the coverage, quality, and freshness of the available job dataset.
- Location relevance uses keyword-based heuristics and does not guarantee that a role is available to applicants in a particular country.
- The current test folder does not contain automated test files.

## 11. Future Enhancements

- Add automated unit and API tests.
- Improve job-description skill extraction and normalization.
- Expand job coverage across Indian locations and remote opportunities.
- Improve resume parsing and evidence-based feedback.
- Add interactive dashboards and recommendation explanations.

## 12. Conclusion

CareerLens-AI demonstrates how resume analysis, database-driven job matching, skill-gap identification, and personalized learning recommendations can be combined into a career intelligence application.
