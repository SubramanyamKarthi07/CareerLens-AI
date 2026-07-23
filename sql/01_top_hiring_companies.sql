-- ==========================================================
-- Query Name : Top Hiring Companies
-- Project    : CareerLens-AI
-- Author     : Subramanyam Karthi
-- Description:
--     Displays the companies with the highest number
--     of job postings.
-- ==========================================================

SELECT
    c.company_name,
    COUNT(jp.job_id) AS total_jobs
FROM job_postings jp
JOIN companies c
    ON jp.company_id = c.company_id
GROUP BY c.company_name
ORDER BY total_jobs DESC
LIMIT 10;