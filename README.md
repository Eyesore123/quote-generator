## Quote Generator

This is my first Angular project. And my first Python project if pygame tutorials do not count (lol). I don't know why I'm calling it Quote Generator, I guess I couldn't come up with a better name. But basically what it does is that the Angular frontend shows quotes that are served from Python backend (Flask).

This is still a work in progress. Right now frontend works and user can check individual random quotes or quote lists by category. There are 570 quotes in total, with pagination. Backend serves the quotes from App.py (Flask). User can search quote by author and quote, but fetch is done on the client side before I write the code for backend.

So I try adding new functionalities using Flask. The goal is to have sub and unsub functions and backend that serves queries using endpoints and send scheduled quotes for those who have an active sub. I might make this a project a little bit larger from what I intended and use PostgreSQL to make a robust and secure database. I'll improve the styles as I go. Most of the python files are still empty.

Backend and frontend are in different folders and run separately. When I get more done I'll try to make it "production ready".

PS. Angular has been a bit hard for me to learn with React background. So many files... I think I get the gist of it but there are still parts that are quite hard to fathom. Perhaps it'll get easier over time.

## What I've learned during this project:

- The basic structure of Angular projects
- How to use Angular CLI
- How routing works in Angular
- Simple Python functions for data manipulation (quotes)

## What is still missing:

- The backend for email subscriptions. Also the backend for API calls to fetch quotes is still missing, not to mention the backend for the actual email sending, scheduling, postgres and so on.
- Option to search quotes (by author name) using server-side fetch.

### I will come update this README.md as I go.