-- ============================
-- CareerLens-AI Database Schema
-- ============================

-- Companies Table
CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) UNIQUE NOT NULL
);

-- Locations Table
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    location_name VARCHAR(255) UNIQUE NOT NULL
);

-- Job Postings Table
CREATE TABLE job_postings (
    job_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company_id INT REFERENCES companies(company_id),
    location_id INT REFERENCES locations(location_id),
    source VARCHAR(100),
    date_posted DATE,
    description TEXT,
    link TEXT
);