-- =====================================================
-- File: loyal_customer_analysis.sql
-- Description: Loyal Customer Analysis
-- Calculates:
--   - Total trips per client
--   - Total trips per driver
-- Database: PostgreSQL
-- Created by: omerfarukbn
-- Changes Date: 2026-02-02
-- =====================================================

SELECT
    t.client_id AS "CLIENT_ID", 
    t.driver_id AS "DRIVER_ID", 
    COUNT(*) AS "TRIP_COUNT" 
FROM trips t
JOIN (
    SELECT
        client_id,
        driver_id
    FROM trips
    GROUP BY client_id, driver_id
    ) p
ON t.client_id = p.client_id
AND t.driver_id = p.driver_id
GROUP BY t.client_id, t.driver_id;

-- =====================================================
-- CLIENT_ID | DRIVER_ID | TRIP_COUNT
-----------+-----------+------------
-- c_287     | d_195     |          1
-- c_137     | d_50      |          1
-- c_317     | d_9       |          2
-- =====================================================