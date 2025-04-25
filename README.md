## Quote Generator

![3](https://github.com/user-attachments/assets/356e024a-63ac-4bb4-9411-c0e1fa688815)


This is my first Angular project. And my first Python project if pygame tutorials do not count (lol). I don't know why I'm calling it Quote Generator, I guess I couldn't come up with a better name. But basically what it does is that the Angular frontend shows quotes that are served from Python backend (Flask).

This is still a work in progress. Right now frontend works and users can browse individual random quotes or quote lists by category. There are 600 quotes in total, with pagination. Backend serves the quotes with Flask. User can search quote by author and quote, but fetch is done on the client side before I write the code for backend.

I will later try adding new functionalities using Flask. Sub and unsub functions should work now, but the code for email service and scheduling is still missing. Backend that serves queries using endpoints and should - when it is ready - send scheduled quotes for those who have an active sub. I'm using PostgreSQL to make a robust and secure database. I'll improve the styles as I go. Some of the Python files are still empty. Flask-SQLAlchemy is used to connect to the database, to create the tables and migrate them. Migration works very similar to how it's done in Laravel.

Backend and frontend are in different folders and run separately. When I get more done I'll try to make it "production ready".

PS. Angular has been a bit hard for me to learn with React background. So many files... Module imports? I think I get the gist of it but there are still parts that are quite hard to fathom. Perhaps it'll get easier over time.

## What I've learned during this project:

- The basic structure of Angular projects
- How to use Angular CLI
- How routing works in Angular
- Simple Python functions for data manipulation (quotes)
- Flask commands

## What is still under work:

- The backend for email subscriptions. Also the backend for API calls to fetch quotes on the server-side is still missing.
- First and last page buttons for pagination

![4](https://github.com/user-attachments/assets/bff4dc16-eb48-417c-9c12-35a4f62d6272)


### I will update this README.md as I make progress.
