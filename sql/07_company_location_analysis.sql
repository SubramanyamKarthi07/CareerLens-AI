-- ==========================================================
-- Query Name      : Company-wise Hiring by Location
-- Project         : CareerLens-AI
-- Author          : Subramanyam Karthi
-- Business Question:
--     Which companies are hiring the most in different locations?
-- Tables Used:
--     job_postings, companies, locations
-- ==========================================================

SELECT
    c.company_name,
    l.location_name,
    COUNT(jp.job_id) AS total_jobs
FROM job_postings jp
JOIN companies c
    ON jp.company_id = c.company_id
JOIN locations l
    ON jp.location_id = l.location_id
GROUP BY
    c.company_name,
    l.location_name
ORDER BY total_jobs DESC
LIMIT 15;