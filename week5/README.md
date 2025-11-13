## Task 2: Create database and table in your MySQL server

### ● Create a new database named website .
### SQL 語句
```sql
create database website;
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task2-Create%20a%20new%20database%20named%20website..jpg)
### ● Create a new table named member , in the website database, designed as below:
### SQL 語句
```sql
create table member(
id int unsigned primary key auto_increment,
name varchar(254) not null,
email varchar(254) not null,
password varchar(254) not null,
follower_count int unsigned not null default 0,
time datetime not null DEFAULT CURRENT_TIMESTAMP 
);
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task2-Create%20a%20new%20table%20named%20member%20%2C%20in%20the%20website%20database%2C%20designed%20as%20below.jpg)


## Task 3: SQL CRUD
### ● INSERT a new row to the member table where name, email and password must be set to test , test@test.com , and test . INSERT additional 4 rows with arbitrary data.
### SQL 語句
```sql
insert into member(id, name, email, password, follower_count) values (1, 'test', 'test@test.com', 'test', 5);
insert into member(name, email, password, follower_count) values ('Nicole', 'nicole@test.com', 'abc', 50);
insert into member(name, email, password, follower_count) values ('Emily', 'emily@test.com', 'cba', 30);
insert into member(name, email, password, follower_count) values ('Penny', 'penny@test.com', 'hub', 3);
insert into member(name, email, password, follower_count) values ('Jenny', 'jenny@test.com', 'def', 5566);
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task3-INSERT%20a%20new%20row%20to%20the%20member%20table%20where%20name%2C%20email%20and%20password%20must%20be%20set%20to%20test%20%2C%20test%40test.com%20%2C%20and%20test%20.%20INSERT%20additional%204%20rows%20with%20arbitrary%20data.jpg)
### ● SELECT all rows from the member table.
### SQL 語句
```sql
select * from member;
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task3-SELECT%20all%20rows%20from%20the%20member%20table.jpg)
### ● SELECT all rows from the member table, in descending order of time.
### SQL 語句
```sql
select * from member order by time desc;
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task3-SELECT%20all%20rows%20from%20the%20member%20table%2C%20in%20descending%20order%20of%20time.jpg)
### ● SELECT total 3 rows, second to fourth, from the member table, in descending order of time. Note: it does not mean SELECT rows where id are 2, 3, or 4.
### SQL 語句
```sql
select * from member order by time desc 
limit 3 offset 1;
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task3-SELECT%20total%203%20rows%2C%20second%20to%20fourth%2C%20from%20the%20member%20table%2C%20in%20descending%20order%20of%20time.jpg)
### ● SELECT rows where email equals to test@test.com .
### SQL 語句
```sql
select * from member where email='test@test.com';
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task3-SELECT%20rows%20where%20email%20equals%20to%20test%40test.com.jpg)
### ● SELECT rows where name includes the es keyword.
### SQL 語句
```sql
select * from member where name like '%es%';
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task3-SELECT%20rows%20where%20name%20includes%20the%20es%20keyword.jpg)
### ● SELECT rows where email equals to test@test.com and password equals to test .
### SQL 語句
```sql
select * from member where email='test@test.com' and password='test';
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task3-SELECT%20rows%20where%20email%20equals%20to%20test%40test.com%20and%20password%20equals%20to%20test.jpg)
### ● UPDATE data in name column to test2 where email equals to test@test.com .
### SQL 語句
```sql
update member set name='test2' where email='test@test.com';
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task3-UPDATE%20data%20in%20name%20column%20to%20test2%20where%20email%20equals%20to%20test%40test.comjpg.jpg)


## Task 4: SQL Aggregation Functions
### ● SELECT how many rows from the member table.
### SQL 語句
```sql
select count(*) from member;
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task4-SELECT%20how%20many%20rows%20from%20the%20member%20table.jpg)
### ● SELECT the sum of follower_count of all the rows from the member table.
### SQL 語句
```sql
select sum(follower_count) from member;
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task4-SELECT%20the%20sum%20of%20follower_count%20of%20all%20the%20rows%20from%20the%20member%20table.jpg)
### ● SELECT the average of follower_count of all the rows from the member table.
### SQL 語句
```sql
select avg(follower_count) from member;
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task4-SELECT%20the%20average%20of%20follower_count%20of%20all%20the%20rows%20from%20the%20member%20table.jpg)
### ● SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.
### SQL 語句
```sql
SELECT AVG(follower_count) AS avg_top2
FROM (
  SELECT follower_count
  FROM member
  ORDER BY follower_count DESC
  LIMIT 2
) top2;
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task4-SELECT%20the%20average%20of%20follower_count%20of%20the%20first%202%20rows%2C%20in%20descending%20order%20of%20follower_count%2C%20from%20the%20member%20table.jpg)


## Task 5: SQL JOIN
### ● Create a new table named message , in the website database. designed as below:
### SQL 語句
```sql
create table message(
id int unsigned primary key auto_increment,
member_id int unsigned not null,
foreign key(member_id) references member(id),
content varchar(65534) not null,
like_count int unsigned not null default 0,
time datetime not null default current_timestamp
);
insert into message(id, member_id, content, like_count) values (1, 5, 'HTML', 10);
insert into message(member_id, content, like_count) values (4, 'CSS', 30);
insert into message(member_id, content, like_count) values (3, 'Javascript', 50);
insert into message(member_id, content, like_count) values (2, 'Python', 87);
insert into message(member_id, content, like_count) values (1, 'FastAPI', 66);
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task5-Create%20a%20new%20table%20named%20message%20%2C%20in%20the%20website%20database.%20designed%20as%20below.jpg)
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task5-insert%20into%20message.jpg)
### ● SELECT all messages, including sender names. We have to JOIN the member table to get that.
### SQL 語句
```sql
select * 
from message
join member on message.member_id=member.id
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task5-SELECT%20all%20messages%2C%20including%20sender%20names.%20We%20have%20to%20JOIN%20the%20member%20table%20to%20get%20that.jpg)
### ● SELECT all messages, including sender names, where sender email equals to test@test.com . We have to JOIN the member table to filter and get that.
### SQL 語句
```sql
select * 
from message
join member on message.member_id=member.id and member.email='test@test.com';
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task5-SELECT%20all%20messages%2C%20including%20sender%20names%2C%20where%20sender%20email%20equals%20to%20test%40test.com%20.%20We%20have%20to%20JOIN%20the%20member%20table%20to%20filter%20and%20get%20that.jpg)
### ● Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender email equals to test@test.com .
### SQL 語句
```sql
select member.email, avg(like_count)
from message
join member on message.member_id=member.id and member.email='test@test.com';
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task5-Use%20SELECT%2C%20SQL%20Aggregation%20Functions%20with%20JOIN%20statement%2C%20get%20the%20average%20like%20count%20of%20messages%20where%20sender%20email%20equals%20to%20test%40test.com.jpg)
### ● Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender email.
### SQL 語句
```sql
select member.email, avg(like_count)
from message
join member on message.member_id=member.id
group by member.email;
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task5-Use%20SELECT%2C%20SQL%20Aggregation%20Functions%20with%20JOIN%20statement%2C%20get%20the%20average%20like%20count%20of%20messages%20GROUP%20BY%20sender%20email.jpg)


