CREATE TABLE IF NOT EXISTS studies (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    start_date DATE
);

CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    birthdate DATE,
    study_id INT REFERENCES studies(id)
);

CREATE OR REPLACE VIEW study_summary AS
SELECT 
    s.id,
    s.title,
    COUNT(p.id) AS patient_count
FROM studies s
LEFT JOIN patients p ON p.study_id = s.id
GROUP BY s.id;
