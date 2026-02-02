-- =====================================================
-- File: driver_performance_report.sql
-- Description: Driver Performance Report
-- Calculates:
--   - Total active days per driver
--   - Success rate based on status = 'done'
-- Database: PostgreSQL
-- Created by: omerfarukbn
-- Changes Date: 2026-02-02
-- =====================================================

SELECT
    driver_id AS "DRIVER_ID",
    COUNT(*) AS "TOTAL_DAYS", 
    ROUND( 100.0 * SUM(done_count) / SUM(total_count), 0 ) AS "SUCCESS_RATE"
FROM ( 
    SELECT driver_id, 
        DATE(trip_date) AS trip_day, 
        COUNT(*) AS total_count, 
        COUNT(*) FILTER (WHERE status = 'done') AS done_count 
    FROM trips 
    GROUP BY driver_id, DATE(trip_date) 
    ) t 
GROUP BY driver_id 
ORDER BY driver_id;


-- =====================================================
-- DRIVER_ID | TOTAL_DAYS | SUCCESS_RATE
-----------+------------+--------------
-- d_1       |        258 |           83
-- d_10      |        274 |           86
-- d_100     |        217 |           62
-- =====================================================
