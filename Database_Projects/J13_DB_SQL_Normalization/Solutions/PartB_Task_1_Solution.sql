/*
This SQL file contains the solutions to IFB105 2019 Assignment 2B part 1 that
involves creating a University database, associated tables and constraints
*/

-- Creating database University and using it
CREATE DATABASE IF NOT EXISTS `University`;

USE `University`;


/*
Deleting any previously created table called Staff
Creating a new table called Staff
Adding the constraints:
    1. Staff ID is a 7 digit auto incrementing number
    2. primary key = Staff ID
*/
DROP TABLE IF EXISTS `Staff`;

CREATE TABLE `Staff` (
  `Staff_id` int(7) NOT NULL AUTO_INCREMENT,
  `firstName` varchar(50) DEFAULT NULL,
  `surname` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Staff_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*
Deleting any previously created table called Student
Creating a new table called Student
Adding the constraints:
 1. Student ID is a 7 digit auto incrementing number
 2. primary key = Student ID
*/
DROP TABLE IF EXISTS `Student`;

CREATE TABLE `Student` (
  `Student_id` int(7) NOT NULL AUTO_INCREMENT,
  `firstName` varchar(50) DEFAULT NULL,
  `surname` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*
Deleting any previously created table called Unit
Creating a new table called Unit
Adding the constraints:
    1. Staff ID is a 7 digit number
    2. primary key = Unit_code
    3. Foreign key staff_id references Staff table
    4. Unit code contains 3 numbers and then 3 letter
*/
DROP TABLE IF EXISTS `Unit`;

CREATE TABLE `Unit` (
  `Unit_code` varchar(6) NOT NULL,
  `Staff_id` int(7) DEFAULT NULL,
  `UnitName` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Unit_code`),
  CONSTRAINT `unit_staff_id` FOREIGN KEY (`Staff_id`) REFERENCES `Staff` (`Staff_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `unit_code_format` CHECK (`Unit_code` LIKE '[0-9][0-9][0-9][A-Z][A-Z][A-Z]')
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*
Deleting any previously created table called Taught_by
Creating a new table called Taught_by
Adding the constraints:
    1. Unit code, staff id and week together form the primary key
    2. Foreign key unit_code references Unit table
    3. Foreign key staff_id references Staff table
    4. Week is an integer between 1 and 13
*/
DROP TABLE IF EXISTS `Taught_by`;

CREATE TABLE `Taught_by` (
  `Unit_code` varchar(6) NOT NULL,
  `Staff_id` int(7) NOT NULL,
  `Week` int NOT NULL,
  PRIMARY KEY (`Unit_code`, `Staff_id`, `Week`),
  CONSTRAINT `taught_by_unit_code` FOREIGN KEY (`Unit_code`) REFERENCES `Unit` (`Unit_code`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `taught_by_staff_id` FOREIGN KEY (`Staff_id`) REFERENCES `Staff` (`Staff_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Week_format` CHECK (`Week` >= 1 AND `Week` <=13)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*
Deleting any previously created table called TuteGroup
Creating a new table called TuteGroup
Adding the constraints:
    1. TuteGroup_code form the primary key
    2. Foreign key unit_code references Taught_by table
    3. DayHrCode is a datetime field
    4. Room_Nr is an int with a default of 0
*/
DROP TABLE IF EXISTS `TuteGroup`;

CREATE TABLE `TuteGroup` (
  `TuteGroup_code` varchar(50) NOT NULL,
  `Unit_code` varchar(6) NOT NULL,
  `DayHrCode` datetime NOT NULL,
  `Room_Nr` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`TuteGroup_code`),
  CONSTRAINT `TuteGroup_unit_code` FOREIGN KEY (`Unit_code`) REFERENCES `Taught_by` (`Unit_code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*
Deleting any previously created table called TuteGroup_List
Creating a new table called TuteGroup_List
Adding the constraints:
    1. TuteGroup_code and Student_Nr together form the primary key
    2. Foreign key TuteGroup_code references TuteGroup table
    3. Foreign key Student_Nr references Student table
*/
DROP TABLE IF EXISTS `TuteGroup_List`;

CREATE TABLE `TuteGroup_List` (
  `TuteGroup_code` varchar(50) NOT NULL,
  `Student_Nr` int(7) NOT NULL,
  PRIMARY KEY (`TuteGroup_code`, `Student_Nr`),
  CONSTRAINT `TuteGroup_List_TuteGroup_code` FOREIGN KEY (`TuteGroup_code`) REFERENCES `TuteGroup` (`TuteGroup_code`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `TuteGroup_List_Student_Nr` FOREIGN KEY (`Student_Nr`) REFERENCES `Student` (`Student_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
