SELECT * FROM ship_sales_data;



-- TOTAL SALES BY STATES
SELECT 
    state,
    SUM(sales) as Revenue
FROM ship_sales_data
GROUP BY state
ORDER BY Revenue DESC;


-- TOTAL REVENUE BY CITY WITHIN STATES
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


-- AVERAGE SHIPPING TIME (DAYS) AFTER THE SUBMISSION OF THE ORDER PER STATE
WITH AVERAGE_SHIP_TIME AS (
    SELECT
        state,
        ROUND(AVG((ship_date::date) - (order_date::date)), 1) as average_ship_days
    FROM ship_sales_data
    GROUP BY state
) 
SELECT
    state,
    average_ship_days
FROM AVERAGE_SHIP_TIME
ORDER BY average_ship_days DESC;


-- TOP-SELLING CATEGORY BY STATE
WITH TOP_CATEGORY AS (
    SELECT
        state,
        category,
        SUM(sales) AS Revenue
    FROM ship_sales_data
    GROUP BY state, category
),
RANKED_CATEGORY AS (
    SELECT
        state,
        category,
        Revenue,
        ROW_NUMBER() OVER (PARTITION BY state ORDER BY Revenue DESC) AS rn
    FROM TOP_CATEGORY
)
SELECT
    state,
    category,
    Revenue AS category_revenue
FROM RANKED_CATEGORY
WHERE rn = 1
ORDER BY category_revenue DESC;
