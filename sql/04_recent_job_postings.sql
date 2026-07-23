-- ==========================================================
-- Query Name      : Recent Job Postings
-- Project         : CareerLens-AI
-- Author          : Subramanyam Karthi
-- Business Question:
--     What are the latest job postings available?
-- Tables Used:
--     job_postings, companies, locations
-- ==========================================================

SELECT
    jp.job_id,
    jp.title,
    c.company_name,
    l.location_name,
    jp.date_posted
FROM job_postings jp
JOIN companies c
    ON jp.company_id = c.company_id
JOIN locations l
    ON jp.location_id = l.location_id
ORDER BY jp.date_posted DESC
LIMIT 10;