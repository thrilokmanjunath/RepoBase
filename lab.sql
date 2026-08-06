CREATE DATABASE lab_1_2_3;
USE lab_1_2_3;
CREATE TABLE States (
    State_ID INT PRIMARY KEY,
    State_Name VARCHAR(100) NOT NULL,
    Region VARCHAR(50) NOT NULL -- North, South, East, West, Central, NE
);


CREATE TABLE Cities (
    City_ID INT PRIMARY KEY,
    City_Name VARCHAR(100) NOT NULL,
    State_ID INT,
    Population_Crores DECIMAL(3, 2), -- Population in crores (e.g., 2.30 for 2.3 crore)
    Is_Capital BOOLEAN,
    FOREIGN KEY (State_ID) REFERENCES States(State_ID)
);

CREATE TABLE Archived_Cities (
    City_Name VARCHAR(100) NOT NULL,
    Population_Crores DECIMAL(3, 2)
);

INSERT INTO States (State_ID, State_Name, Region) VALUES
(101, 'Maharashtra', 'West'),
(102, 'Tamil Nadu', 'South'),
(103, 'Uttar Pradesh', 'North'),
(104, 'West Bengal', 'East'),
(105, 'Gujarat', 'West');


INSERT INTO Cities (City_ID, City_Name, State_ID, Population_Crores, Is_Capital) VALUES
(201, 'Mumbai', 101, 2.30, TRUE),
(202, 'Pune', 101, 0.74, FALSE),
(203, 'Chennai', 102, 1.15, TRUE),
(204, 'Coimbatore', 102, 0.35, FALSE),
(205, 'Lucknow', 103, 0.38, TRUE),
(206, 'Kanpur', 103, 0.32, FALSE),
(207, 'Kolkata', 104, 1.55, TRUE),
(208, 'Surat', 105, 0.69, FALSE),
(209, 'Ahmedabad', 105, 0.88, FALSE),
(210, 'Nashik', 101, 0.18, FALSE);


INSERT INTO Archived_Cities (City_Name, Population_Crores) VALUES
('Madras', 0.95), -- Old name for Chennai
('Calcutta', 1.40), -- Old name for Kolkata
('Patna', 0.25);



SELECT City_Name, Population_Crores FROM Cities;


SELECT * FROM Cities WHERE Population_Crores > 1.00;--


SET SQL_SAFE_UPDATES = 0;
UPDATE Cities SET Is_Capital = TRUE WHERE City_Name = 'Ahmedabad';


DELETE FROM Cities WHERE City_Name = 'Nashik';


SELECT COUNT(City_ID) AS Total_Cities FROM Cities;--


SELECT 
    s.State_Name, 
    SUM(c.Population_Crores) AS Total_Population
FROM 
    Cities c 
JOIN 
    States s ON c.State_ID = s.State_ID 
GROUP BY 
    s.State_Name;--


SELECT 
    Region, 
    AVG(Population_Crores) AS Avg_Pop
FROM 
    Cities c 
JOIN 
    States s ON c.State_ID = s.State_ID 
GROUP BY 
    Region 
HAVING 
    AVG(Population_Crores) < 0.80;
    
    
    
