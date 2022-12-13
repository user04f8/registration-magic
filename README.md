# registration-magic
Automate BU Registration

##
- To build this project you must have python and flutter installed on your system. To run the project go to the ui folder and type the command:

-   $flutter run lib/main.dart

## Running the project

Open the flutter app and run the backend server.

Flutter
- open the built app available for Windows, Android, or iOS -- for developement, install Flutter and build main.dart, using `flutter pub get` to get dependencies

Backend
- `cd backend`
- `py main.py`
See `backend\README.md` for more details on running the backend server

## Project Structure

parenthesis = optional

- Flutter frontend
  - Ability to search for and add courses, stored locally (or to a server)
  - Ability to schedule registration (when does your registration open?)
  - Ability to send this data to the backend
  - (User login page)
- Python backend
  - Ability to send requests from backend to Student Link to make the registration requests
  - Storing all SelectIt IDs for every course
    - web scraping
    - ** can scrape from value token of the input tag defining the checkbox TL;DR use the checkbox to get SelectIt info **
- (Firebase database, or MongoDB -- can decide later for storing user data through authentication)

## Application Demo
-   https://www.youtube.com/watch?v=ln91Cqp5xLY

## Team Members
-   Cynthia Young: mcyoung@bu.edu
-   Sadman Kabir: kabirs@bu.edu
-   Nathan Clark: nbclark@bu.edu
-   Peter West: flibble@bu.edu
-   Oluwaseun Angelo Soyannwo: seun@bu.edu
