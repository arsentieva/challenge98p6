### PostgreSQL Database setup:
=> create user: 
   create user drop_token_admin with password 'password' createdb;
=> create database: 
   create database drop_token_db with owner drop_token_admin;

!!! create a .env file in the root of your cloned repo directory, copy values from .env.example into .env 