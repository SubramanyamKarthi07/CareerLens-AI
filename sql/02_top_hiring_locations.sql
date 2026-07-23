-- ==========================================================
-- Query Name : Top Hiring Locations
-- Project    : CareerLens-AI
-- Author     : Subramanyam Karthi
-- Description:
--     Displays the locations with the highest number
--     of job postings.
-- ==========================================================

SELECT
    l.location_name,
    COUNT(jp.job_id) AS total_jobs
FROM job_postings jp
JOIN locations l
    ON jp.location_id = l.location_id
GROUP BY l.location_name
ORDER BY total_jobs DESC
LIMIT 10;