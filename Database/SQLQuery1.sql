USE Northwind -- select domain have data - one time only connect with 1 data

/*SELECT * FROM Employees -- output is a table
WHERE Region IS NOT NULL 
AND ReportsTo IS NOT NULL

--SELECT N'PHIC: ' + CONVERT(NVARCHAR, (YEAR(GETDATE()) - 2006)) + N'YEARS OLD' AS 'STUDENT'
SELECT DISTINCT ORDERS.OrderID,
Employees.LastName,
Employees.FirstName
FROM ORDERS
RIGHT JOIN Employees ON ORDERS.EmployeeID = Employees.EmployeeID
ORDER BY ORDERS.OrderID */

SELECT * FROM Orders WHERE Freight BETWEEN 100 AND 500;

SELECT * FROM Orders WHERE ShipCountry IN ('UK', 'France', 'USA');

SELECT * FROM Orders WHERE ShipCountry NOT IN ('UK', 'France', 'USA');

SELECT * FROM Orders WHERE YEAR(ShippedDate) = '1996' AND MONTH(ShippedDate) NOT IN ('6', '7', '8', '9');

-- IN only use for set and not suitable for range like the range from (10 to 20) because it can be alot of real numbers 
-- this time use BETWEEN
-- Not contain data ==> not have value ==> cannot compare ==> use IS NULL or IS NOT NULL to filter the data

SELECT * FROM Employees WHERE Title = 'Sales Representative' AND Region IS NOT NULL

SELECT 
	CustomerID,
	Phone,
	Fax,
	Region
FROM Customers 
WHERE Region IS NOT NULL AND Fax IS NOT NULL AND Country IN ('UK', 'France', 'USA')
ORDER BY CustomerID


-- DO NOT GROUP BY KEY Because they are unique
-- COUNT Employee By City

SELECT City, COUNT(City) AS [No City] FROM Employees 
GROUP BY City 
HAVING COUNT(City) >= 2
-- SELECT <Col> FROM <Table> WHERE <clause> GROUP BY <Col> HAVING <st> ORDER BY <Col>


-- Count Empployee of London and Seattle

SELECT City, COUNT(*) FROM Employees WHERE City IN ('London', 'Seattle') GROUP BY City HAVING COUNT(*) >= 3
SELECT * FROM Orders
SELECT ShipCity, COUNT(*) FROM Orders
GROUP BY ShipCity
ORDER BY COUNT(*) DESC

SELECT * FROM Categories
SELECT * FROM Products
-- Count products by categories
SELECT C.CategoryName, COUNT(P.ProductID) FROM Categories AS C
JOIN Products AS P ON P.CategoryID = C.CategoryID 
GROUP BY CategoryName

SELECT COUNT(*) FROM Products

-- Country with more than 10 orders
SELECT ShipCountry, COUNT(*) FROM Orders 
GROUP BY ShipCountry
HAVING COUNT(*) >= ALL (
	SELECT COUNT(ShipCountry) FROM Orders 
	GROUP BY ShipCountry
)


-- Number of orders from 3 countries

SELECT ShipCountry, COUNT(*) AS [No Orders] FROM Orders WHERE ShipCountry IN ('France', 'USA', 'UK') 
GROUP BY ShipCountry -- Show each orders from each country
HAVING COUNT(*) > 100


SELECT City, COUNT(*) FROM Employees 
GROUP BY City
HAVING COUNT(*) >= ALL
	(
		SELECT COUNT(City) FROM Employees
		GROUP BY City
	)

SELECT MAX(Valu) AS Max_ FROM (
	SELECT COUNT(*) AS Valu FROM Orders
	GROUP BY ShipCity
	) AS Sub

-- Orders have freight >= AVG
SELECT COUNT(*) FROM
	(
		SELECT * FROM Orders WHERE Freight >= (
							SELECT AVG(Freight) FROM Orders 
							)
	) AS Sub

select * from Orders
select * from [Order Details]
select * from Products
go 


	
create view [Invoice Details]
as 
(
select
		d.orderid as InvoiceID,
		p.ProductName,
		d.Quantity,
		d.UnitPrice,
		cast(SUM((1 - d.discount) * d.quantity * d.unitprice) as decimal(10, 2)) as TotalPrice
	from [Order Details] d
	join products p on p.ProductID = d.productID
	group by d.OrderID, p.ProductName, d.Quantity,d.UnitPrice
)
select * from [Invoice Details]
go 
create view Invoices
as 
(
	select 
		o.orderid as InvoiceID,
		o.CustomerID,
		Cast(SUM((1 - d.discount) * d.quantity * d.unitprice) as decimal(10, 2)) as Total 
	from Orders o
	join [Order Details] d on o.OrderID = d.OrderID
	group by o.OrderID, o.CustomerID
)
go 

select * from Invoices