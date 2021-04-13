/* Use pg_prewarm to fill up the database cache */
CREATE EXTENSION pg_prewarm;
SELECT * FROM pg_prewarm('a3.shootings');

/* Create a materialized view for the query that populates the bar chart */
CREATE MATERIALIZED VIEW a3.month_year_count_matview AS
    SELECT DISTINCT
      EXTRACT(MONTH FROM date)::INT AS month,
      EXTRACT(YEAR FROM date)::INT AS year,
      COUNT(id)
    FROM a3.shootings
    GROUP BY month, year
    ORDER BY year, month;

/* Create indexes for major attributes that have many unique values */
CREATE INDEX idx ON a3.shootings(id);
CREATE INDEX date_idx ON a3.shootings(date);
CREATE INDEX race_idx ON a3.shootings(race);
CREATE INDEX age_group_idx ON a3.shootings(age_group);
CREATE INDEX gender_idx ON a3.shootings(gender);
CREATE INDEX flee_idx ON a3.shootings(flee);

/* A3 Permissions */
GRANT USAGE ON SCHEMA a3 TO cmsc828d;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA a3 TO cmsc828d;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA a3 TO cmsc828d;
