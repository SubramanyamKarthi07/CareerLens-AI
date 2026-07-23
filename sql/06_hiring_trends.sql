-- ==========================================================
-- Query Name      : Hiring Trends
-- Project         : CareerLens-AI
-- Author          : Subramanyam Karthi
-- Business Question:
--     How many jobs were posted each day?
-- Tables Used:
--     job_postings
-- ==========================================================

SELECT
    date_posted,
    COUNT(job_id) AS total_jobs
FROM job_postings
GROUP BY date_posted
ORDER BY date_posted;