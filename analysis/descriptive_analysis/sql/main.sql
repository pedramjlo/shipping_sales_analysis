SELECT * FROM ship_sales_data;



-- TOTAL SALES BY STATES
SELECT 
    state,
    SUM(sales) as Revenue
FROM ship_sales_data
GROUP BY state
ORDER BY Revenue DESC;


-- TOTAL SALES BY CITY WITHIN STATES
WITH SALES_PER_CITY AS (
    SELECT
        city,
        state,
        SUM(sales) as Revenue
    FROM ship_sales_data
    GROUP BY city, state
)
SELECT
    city,
    state,
    Revenue
FROM SALES_PER_CITY
ORDER BY state, Revenue DESC;