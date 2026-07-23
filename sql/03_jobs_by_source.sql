-- ==========================================================
-- Query Name      : Jobs by Source
-- Project         : CareerLens-AI
-- Author          : Subramanyam Karthi
-- Business Question:
--     Which job platform provides the most job postings?
-- Tables Used:
--     job_postings, sources
-- ==========================================================

SELECT
    s.source_name,
    COUNT(jp.job_id) AS total_jobs
FROM job_postings jp
JOIN sources s
    ON jp.source_id = s.source_id
GROUP BY s.source_name
ORDER BY total_jobs DESC;