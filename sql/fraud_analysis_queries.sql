-- Use Database
USE financial_fraud_analytics;

-- 1. Total Transactions
SELECT COUNT(*) AS Total_Transactions
FROM paysim_feature_engineered;

-- 2. Total Fraud Transactions
SELECT COUNT(*) AS Fraud_Transactions
FROM paysim_feature_engineered
WHERE isFraud = 1;

-- 3. Fraud Rate
SELECT
ROUND(
SUM(isFraud) * 100.0 / COUNT(*),2
) AS Fraud_Rate
FROM paysim_feature_engineered;

-- 4. Transaction Type Distribution
SELECT
type,
COUNT(*) AS Total
FROM paysim_feature_engineered
GROUP BY type;

-- 5. Fraud by Transaction Type
SELECT
type,
COUNT(*) AS Fraud_Count
FROM paysim_feature_engineered
WHERE isFraud = 1
GROUP BY type;

-- 6. Average Transaction Amount
SELECT
AVG(amount) AS Average_Amount
FROM paysim_feature_engineered;

-- 7. Highest Transaction
SELECT
MAX(amount) AS Highest_Transaction
FROM paysim_feature_engineered;

-- 8. High Value Transactions
SELECT
COUNT(*) AS High_Value_Transactions
FROM paysim_feature_engineered
WHERE high_value_transaction = 1;

-- 9. Top 10 Largest Transactions
SELECT *
FROM paysim_feature_engineered
ORDER BY amount DESC
LIMIT 10;

-- 10. Daily Fraud Trend
SELECT
day,
SUM(isFraud) AS Fraud_Count
FROM paysim_feature_engineered
GROUP BY day
ORDER BY day;

-- 11. Hourly Fraud Trend
SELECT
hour,
SUM(isFraud) AS Fraud_Count
FROM paysim_feature_engineered
GROUP BY hour
ORDER BY hour;

-- 12. Zero Balance Sender Analysis
SELECT
zero_balance_sender,
COUNT(*) AS Total
FROM paysim_feature_engineered
GROUP BY zero_balance_sender;

-- 13. Zero Balance Receiver Analysis
SELECT
zero_balance_receiver,
COUNT(*) AS Total
FROM paysim_feature_engineered
GROUP BY zero_balance_receiver;

-- 14. Average Amount by Transaction Type
SELECT
type,
ROUND(AVG(amount),2) AS Average_Amount
FROM paysim_feature_engineered
GROUP BY type;

-- 15. Fraud Percentage by Transaction Type
SELECT
type,
ROUND(
SUM(isFraud)*100.0/COUNT(*),2
) AS Fraud_Percentage
FROM paysim_feature_engineered
GROUP BY type;