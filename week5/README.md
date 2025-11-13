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
update member set name='test2' where email='test@test.com' and id=1;
```
### 執行結果
![Task 2 結果截圖](https://github.com/pei-IT/stage_I_mission_project/blob/main/week5/screenshots/Task3-UPDATE%20data%20in%20name%20column%20to%20test2%20where%20email%20equals%20to%20test%40test.comjpg.jpg)






