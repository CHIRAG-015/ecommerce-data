SELECT
    u.name AS user_name,
    o.order_id,
    p.name AS product_name,
    oi.quantity,
    o.total_amount,
    pay.method AS payment_method,
    pay.status AS payment_status
FROM users AS u
JOIN orders AS o ON o.user_id = u.user_id
JOIN order_items AS oi ON oi.order_id = o.order_id
JOIN products AS p ON p.product_id = oi.product_id
JOIN payments AS pay ON pay.order_id = o.order_id
ORDER BY o.order_id
LIMIT 20;

