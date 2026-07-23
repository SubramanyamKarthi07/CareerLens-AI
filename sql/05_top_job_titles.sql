-- ==========================================================
-- Query Name      : Top Job Titles
-- Project         : CareerLens-AI
-- Author          : Subramanyam Karthi
-- Business Question:
--     Which job titles appear most frequently?
-- Tables Used:
--     job_postings
-- ==========================================================

SELECT
    title,
    COUNT(*) AS total_jobs
FROM job_postings
GROUP BY title
ORDER BY total_jobs DESC
LIMIT 10;