# omg

## Steps to run the project
  - Make sure to have Docker andd Docker compose installed on your system
  - Run `docker-compose build` to build the images
  - Run `docker-compose up` to run the project.
  - For the demo purpose, a seed file is included, which gets executed on each run.


## APIs
  - /<username>/rank - to get a user's current rank.
  - /leaderboard - to get the top rankers
  - /leaderboard/<n> - to get the top n rankers

## Assumptions
  - A user can only play one game at a time.
  - Only active games are shown in leaderboard.
  
