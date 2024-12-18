-- Create database 
create DATABASE simple_login_database;
USE simple_login_database;

-- Create table
-- Table does not allow NULL value
CREATE TABLE Users (
	username VARCHAR(50) NOT NULL,
    id INT NOT NULL PRIMARY KEY,
	age INT NOT NULL,
	password VARCHAR(225) NOT NULL
);
-- View table
SELECT * FROM Users

-- Insert details into 

