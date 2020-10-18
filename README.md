# With Madrid Fullstack Bot

## Status 
![CircleCI](https://circleci.com/gh/victorgrubio/with-madrid-fullstack-bot.svg?style=svg) 
![Build status](https://img.shields.io/circleci/build/gh/victorgrubio/with-madrid-fullstack-bot/main?token=ccf75fe7e2f1925687bae66dc293fe9bfca32eee)
![Docker Pulls](https://img.shields.io/docker/pulls/victorgrubio/bernard-bot-with-madrid)



## Description

Repo that contains the code from the technical test regarding the position of Fullstack developer at With Madrid. It consists on a bot that finds the moment where the SpaceX rocket was launched based on the user answers using a binary search.

You can try it [**here!**](https://t.me/Victorgarciarubio_withmadrid_bot)

Deployed at **Azure** using [**CircleCI**](https://circleci.com) for the CI procedure, via Docker.

Deployment attempt at **Heroku** without success due to authorization issues.

## Code sustainability

I have developed the complete project to be adaptative for multiple deployment scenarios by the use of Docker and environment variables. These elements allows the project to be installed and configured in a flexible way.

Regarding the code, I have moved from the code in the PoC presented in the document of the test to the real implementation. I have used the already created components to handle video information as they were clean and useful implementations. Most of the methods have been removed from these components and extracted to other elements.

The fact that the process is asynchronous instead of the while loop as in the PoC is the most relevant difference for me in terms of the implementation. I had to move the algorithm logic to the trigger action.

The states have been developed from the Guess Number bot available in the BERNARD course. We have developed 4 states to differenciate between the start, the first question, the rest of the questions and when the user finds the frame.

I think the code could be improved in next steps in terms of testing, as I don't have the knowledge yet to test the implementation using this framework. In terms of code quality I think my development is clean and simple, as most of the logic was already implemented in the PoC.

Hope you like my project!

<br> <br>
### Victor Garcia Rubio
Software developer specialized in Python Backend for AI and Devops