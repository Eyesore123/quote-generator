## Quote Generator

![3](https://github.com/user-attachments/assets/356e024a-63ac-4bb4-9411-c0e1fa688815)


This is my first Angular project. And my first Python project if pygame tutorials do not count (lol). I don't know why I'm calling it Quote Generator, I guess I couldn't come up with a better name. But basically what it does is that the Angular frontend shows quotes that are served from Python backend (Flask).

This is still a work in progress. Right now frontend works and users can browse individual random quotes or quote lists by category. There are 600 quotes in total, with pagination. Backend serves the quotes with Flask. User can search quote by author and quote, but fetch is done on the client side before I write the code for backend.

I will later try adding new functionalities. Sub and unsub functions and email scheduling should work now. I'll improve the styles as I go. Flask-SQLAlchemy is used to connect to the database, to create the tables and migrate them. Migration works very similar to how it's done in Laravel.

Backend and frontend are in different folders and run separately. Frontend is hosted on Netlify. Backend is hosted on Render.com. Postgres database is hosted on Neon.

PS. Angular has been a bit hard for me to learn with React background. So many files... and all those module imports... I think I get the gist of it but there are still parts that are quite hard to fathom. You need to be a goddamn wizard to get all the modules, imports and server configurations to work correctly. Perhaps it'll get easier over time, but I would rather use React for future projects with less headache.

## What I've learned during this project:

- The basic structure of Angular projects
- How to use Angular CLI
- How routing works in Angular
- Simple Python functions for data manipulation (quotes)
- Flask commands
- The limitations of Flask's built-in server, which can cause weird issues on debug mode by running multiple processes of scheduler. If I run the scheduler in debug mode, it will send as many emails as it can within a second. It can also print statements like there was no tomorrow. It's similar to how useEffect can run multiple times in React.
- The differences between different servers: Flask, Gunicorn, Waitress
- How to deploy backend API using Flask
- Render.com is not very easy to use when you're working with a single-page application and want to redirect routes through index file. I couldn't get the frontend to work with Render, then I switched to Netlify and boom! - it worked immediately. Setting up the SPA configurations for the server can be a bit tricky.
- My initial plan for quote generator was far too restrictive. App needs to store more data to db than I thought would be required to ensure a good user experience. If I had more experience with PostgreSQL and Python, I could've put the quotes inside a db for improved efficiency, but this approach was fine too since I was better able to understand the differences between using a approach where data is stored in an array and a relational database approach. I've used Firebase databases before, so I could've been more intelligent from the start and turned my quote array into a dictionary-like structure with id:s and keys, but this works too since it's not a lot of data.

## What is still under work:

- I plan to transfer all the quotes to db. Quotes are currently stored in a json file and served on the client-side, but fetched using backend urls.
- Landing page definitely needs better styling + mobile responsiveness.
- I will try using cron jobs to wake up Render backend before it's time to send scheduled emails so I can use the free service.

![4](https://github.com/user-attachments/assets/bff4dc16-eb48-417c-9c12-35a4f62d6272)


### I will update this README.md as I make progress.
