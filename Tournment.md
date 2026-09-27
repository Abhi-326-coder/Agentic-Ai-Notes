# Freefire Game Tournment hosting Website

## About the Game: Freefire

Garena Free Fire is a popular, free-to-play mobile battle royale game developed and published by Garena for Android and iOS

-  Fast-paced 10-minute matches drop 50 players(12 teams with 4 players per team) onto an island to scavenge and survive. Popular modes include Battle Royale and 4v4 Clash Squad.
- Characters: Choose from various unique characters equipped with distinct active and passive abilities that add tactical depth to squad play.
- Accessibility: Engineered with forgiving gunplay and optimized performance to run smoothly on almost any smartphone.
- Free Fire MAX: An enhanced version offering Ultra HD resolutions, upgraded map visuals, and smoother animations via Firelink technology.


## Reason to build
- Me and My friends have decided to host the tournments for freefire game for now

- currently what we have decided or doing is we have a whatsapp group for tournment where all the players have joined and say I want to host tomorrow evening at 7 pm, freefire tournment, we send a message on group and whoever want to join the tournment can register the google form and send the phonepe screenshot of registration amount then we will verify the payment and add him in the tournment 

- when the tournment starts then we will send the tournment or custom id so that whoever joined the tournment can join the custom and we will verify the team members manually, and few of our friends will spectate the game and when the game is finished, we will announce the winners, top 1 to 3 will be distributed with winner amount and our admin will pay back selectively winner amount

- here everything is going manual we don't have track of each team, winners, participants and in future if we want to host more matches and if too many participants comes then that would be a headach to manage them

- In future we may want to host more games like BGMI, valorant and more

## What I expect from the website
- For now a website which solves our problem of tracking the teams and there participants providing them a interface to see events and able to register with completing the payments

- for us providing a admin interface who could create a event, host it and get the payment securly and payback interface to winner paying back there winning amount

- A group chat interface maybe in future, where all the participants can chat or we can tell them the game custom id of each event participants joined by registering

## What tech stacks I would like to go with

- React - frontend
- Express and nodejs - backend
- clerk or Google Oauth - for authentication maybe 
- Email and Password - for authentication
- Mongodb or Postgress - Database 
- Razorpay - Payment method
- Redis - in future for caching

## What My Website will have 

- **Register or SignUp Page:** Where As soon as the player enters need to be registered. In this page, Register with Google or Register with Email and Password will be asked and Registration will be completed. after completion it will redirect fill-form page.

- **Login or SignIn Page:** If player has already registered then he can simply login with Google or by email and password after login completion redirect to dashboard or home page.

- **Fill form Page:** When player completets Sign up then We will need some details like here this website is for hosting freefire tournments So he has to fill details like Team name, logo (optional), leader name, phone number, free-fire id and free-fire in game name and similar details for all the team members(total in a team 4 members will be there) and user fills the form properly.

- **Dashboard or Home Page:** this is the main page where the Registerd or signed in only player will see the Upcoming tournments, Registered Events or tournments, Popular Events and they will see these Events cards having images, name of event, timings and Register button on click takes to event/ tournments details, and where he can pay the entry fee.

- **Tournment Details Page:** when player clicks on the any event card for registration, that would take him to this page, Which will have Overview of that Tournment, Rules of that Tournment and a pay button on click user will pay the entry fee and after successfull Payment completion, he will be added to tournment list and this page will be a