-- Create the database hbnb_dev_db if it doesn't already exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create the user hbnb_dev with password hbnb_dev_pwd if it doesn't already exist
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on the database hbnb_dev_db to the user hbnb_dev
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on the database performance_schema to the user hbnb_dev
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;
