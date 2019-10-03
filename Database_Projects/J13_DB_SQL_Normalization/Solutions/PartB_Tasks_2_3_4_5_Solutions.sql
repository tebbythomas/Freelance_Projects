/*
This SQL file contains the solutions to IFB105 2019 Assignment 2B parts 2, 3, 4
and 5 that query the TreasureHunter Database
*/

--TASK2

--Setting the Database here:
USE `treasurehunters`;


/*
Query 1:

Write a query to list the treasureID, description, points and types of treasures
that contain either ‘brick’ or ‘map’ in their description.
*/

--ANSWER:
SELECT treasureID, description, points, type FROM treasure WHERE description LIKE "%brick%" OR description LIKE "%map%";

/*
Query 2:

Write a query to list the total number of treasures for each treasure type. Your
output should contain the type and the total of each type in ascending order of
the number of types.
*/

--ANSWER:
SELECT type, COUNT(type) AS number_of_treasures FROM treasure GROUP BY type ORDER BY number_of_treasures;

/*
Query 3:

Write a query that lists the name, badgeID and the cost of the most expensive badge.
*/

--ANSWER:
SELECT badgeName, p.badgeID, cost FROM badge AS b, purchase AS p WHERE b.badgeID = p.badgeID AND cost = (SELECT MAX(cost) FROM purchase);

/*
Query 4:

Write a query that lists all badge sales. Your output should show the name of
the badge together with first name, last name and email address of the player(s)
that made the purchase. Sort the list based on the badge name followed by first
name then last name in ascending order.
*/

--ANSWER:
SELECT badgeName, firstName, lastName, email FROM purchase AS pu, badge AS b, player AS pl WHERE pu.badgeID = b.badgeID AND pu.username = pl.username ORDER BY badgeName, firstName, lastName;

/*
Query 5:

Write a query that provides the players’ name (first and last), username and how
many advanced quests they have completed. If a player did not complete any advanced
quests, do not include them in your output.
*/

--ANSWER:
SELECT firstName, lastName, pl.username, COUNT(progress) AS advancedQuestsCompleted FROM player AS pl, playerProgress AS pp WHERE progress LIKE "complete" AND pl.username = pp.username GROUP BY pl.username;

/*
Query 6:

Write a query to produce a report for each store including stores without any
sales. Your result-set should include the following information:
•	the storeID
•	the store name
•	the number of players that have purchased a badge from the store
•	the number of players that have not purchased a badge from the store;
•	the total money spent at the store
•	the most expensive badge a player has purchased at the store
•	the cheapest badge a player has purchased at the store
•	the average price of the items that have been purchased at the store.

*/

--ANSWER:
SELECT store.storeID, storeName, COUNT(DISTINCT purchase.username) AS player_purchase_count, COUNT(DISTINCT player.username)- COUNT(DISTINCT purchase.username) AS player_no_purchase_count, SUM(DISTINCT purchase.cost) AS total_revenue, MAX(purchase.cost) AS most_expensive_purchase , MIN(purchase.cost) AS lease_expensive_purchase, AVG(purchase.cost) AS average_price FROM store LEFT JOIN purchase ON store.storeID = purchase.storeID, player GROUP BY store.storeID;


--TASK 3

/*
Insert:

Write an INSERT command to insert a row into badge table. The badge is called
‘Summer Rain’ and the description should be ‘Beach, sun and holidays’.
*/

--ANSWER:
INSERT INTO `badge` VALUES (18, 'Summer Rain','Beach, sun and holidays');

/*
Delete:

Write a DELETE command to remove all the rows from the player progress table for
which progress is complete.
*/

--ANSWER:
DELETE from playerprogress WHERE progress = 'complete';

/*
Update:

Write an UPDATE comment to change the address of all players with the last name
‘Halpin’ who live at ‘1800 Zelda Street, Linkburb’ to ’72 Evergreen Terrace, Springfield’.
*/

--ANSWER:
UPDATE player SET streetNumber = '72', streetName = 'Evergreen Terrace', suburb = 'Springfield' WHERE lastName = 'Halpin' AND streetNumber = '1800' AND streetName = 'Zelda Street' AND suburb = 'Linkburb';


--TASK 4

/*
Create Index:

Write a command to create an index on story column of the quest table.
*/

--ANSWER:
/*
To avoid the error: Error Code: 1170. BLOB/TEXT column 'story' used in key
specification without a key length
*/
ALTER TABLE quest MODIFY story VARCHAR(255);
CREATE INDEX story_index ON quest(story);

/*
Create View:

Write a command to create a view to list the firstname, lastname and account
creation date of all players that have started a quest but are currently inactive.
*/

--ANSWER:
CREATE VIEW inactive_players AS SELECT firstName, lastName, creationDateTime FROM player, playerprogress WHERE player.username = playerprogress.username AND progress = 'inactive';


--TASK 5

/*
Working as a Database Administrator for MySQL Treasure Hunter database, write
the following commands for two employees namely Lisa and Sri to achieve the
following database security requirements:
*/

/*
A. User Lisa is no longer allowed to add data to the Player table:
*/

--ANSWER:
REVOKE INSERT ON treasurehunters.player FROM 'lisa'@'localhost';

/*
B. User Lisa is no longer allowed to delete records from the Player table:
*/

--ANSWER:
REVOKE DELETE ON treasurehunters.player FROM 'lisa'@'localhost';

/*
C. User Sri must be able to add records to the Quest table:
*/

--ANSWER:
GRANT INSERT ON treasurehunters.quest TO 'sri'@'localhost';

/*
D. User Sri must be able to remove records from the Quest table:
*/

--ANSWER:
GRANT DELETE ON treasurehunters.quest TO 'sri'@'localhost';
