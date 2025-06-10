-- 1.)    Find products with greater than the average quantities across all orders 


SELECT p.product_id, p.product_name, p.quantity
FROM Product p
WHERE p.quantity > (
    SELECT AVG(quantity)
    FROM Orders
);






-- 2.)   Find the top 3 cities with the most customers and their average age:


SELECT city, COUNT(User_ID) as Number_of_Customers, AVG(age) as Average_Age
FROM Customer
GROUP BY city
ORDER BY Number_of_Customers DESC
LIMIT 3;


-- 3.)  Customer who have not added item to wishlists:
SELECT User_ID, first_name, last_name
FROM Customer
WHERE User_ID NOT IN (
    SELECT DISTINCT cart_id
    FROM Wishlist
);


-- 4.)  Find the first name , last name who works as customer or either vendor:













-- 5.)  Find the customers who live in the city with the most customers:


SELECT *
FROM Customer
WHERE city = (
    SELECT city
    FROM (
        SELECT city, COUNT(User_ID) as Number_of_Customers
        FROM Customer
        GROUP BY city
        ORDER BY Number_of_Customers DESC
        LIMIT 1
    ) AS MostPopulatedCity
);


-- 6.) Find the customers who live in the city with the highest average age:


SELECT *
FROM Customer
WHERE city = (
    SELECT city
    FROM (
        SELECT city, AVG(age) as Average_Age
        FROM Customer
        GROUP BY city
        ORDER BY Average_Age DESC
        LIMIT 1
    ) AS CityWithHighestAvgAge
);




-- 7.) Find the customers who have placed orders in more than one location:


SELECT c.User_ID, c.first_name, c.last_name
FROM Customer c
WHERE c.User_ID IN (
    SELECT User_ID
    FROM (
        SELECT User_ID, COUNT(DISTINCT location) AS num_locations
        FROM Orders
        GROUP BY User_ID
    ) AS subquery
    WHERE num_locations > 1
);


-- 8.) Find the product with greater than the average quantities across all orders:


SELECT p.product_id, p.product_name, p.quantity
FROM Product p
WHERE p.quantity > (
    SELECT AVG(quantity)
    FROM Orders
);


-- 9.) Find the number of order for each customer:


SELECT Customer.first_name, Customer.last_name, COUNT(Orders.order_id) AS num_orders
FROM Customer
JOIN Orders ON Customer.User_ID = Orders.cart_id
GROUP BY Customer.User_ID;


-- 10.) find the customer who reside in the city with the highest number of customer per unique customer_ID:


SELECT c1.User_ID, c1.first_name, c1.last_name
FROM Customer c1
WHERE (c1.city, c1.User_ID) IN (
    SELECT city, User_ID
    FROM (
        SELECT city, User_ID, COUNT(*) as count
        FROM Customer
        GROUP BY city, User_ID
        HAVING count = (
            SELECT MAX(count)
            FROM (
                SELECT city, COUNT(*) as count
                FROM Customer
                GROUP BY city, User_ID
            ) AS subquery
            WHERE subquery.city = city
        )
    ) AS c2
);


-- 11.) find the list of cities where the number of customers is more than the number of vendors:


SELECT c.city
FROM Customer c
GROUP BY c.city
HAVING COUNT(c.User_ID) > (
    SELECT COUNT(v.vendor_id)
    FROM Vendor v
    WHERE v.city = c.city
);
-- 12.) find the customer who live in same city as a vendor:


SELECT c.User_ID, c.first_name, c.last_name, c.city
FROM Customer c
JOIN Vendor v ON c.city = v.city;
