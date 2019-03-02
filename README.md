# Blackjack Project
A version of this project is deployed on Heroku, you can start playing it right away by going to
`https://jh-blackjack-ui.herokuapp.com/`.

##Usage

###Play Blackjack Locally
1. Clone the latest master branches of the following repositories:
    - https://github.com/JamesHan1008/blackjack-api
    - https://github.com/JamesHan1008/blackjack-ui
2. Navigate to `blackjack-api` in one command line window, and do:
    - Create a Postgres database locally, and create a user with all privileges
    - Create a `.env` file with the following environment variables:
        - `DJANGO_SETTINGS_MODULE=blackjack_project.settings`
        - `DATABASE_URL=postgres://{username}:{password}@127.0.0.1:5432/{database_name}`
        - `HOST=127.0.0.1`
    - `$ pipenv shell`
    - `$ ./manage.py migrate`
    - `$ ./manage.py runserver`
3. Navigate to `blackjack-ui` in another command line window, and do:
    - `$ npm start`
4. Go to `http://127.0.0.1:3000/` in a browser
    - Use the `Manage Dealers` link to add custom dealer rules to play against
    - Use the `Play Game` link to find a list of dealers to play against

### Test AI Strategies
1. Test existing AI strategies
    - Set up the `blackjack-api` repository using the instructions above
    - Navigate to `blackjack-api` on the command line and run `$ pipenv shell`
    - Evaluate an AI's performance by running `$ ./manage.py evaluate_ai -n [number of games] -a [AI class name]`
2. Create your own AI strategies and test them
    - Create a class that inherits from the `BaseAI` class or any of its subclasses
    - Overwrite the default `decide_bet_amount` and/or `decide_action` to use your own betting and playing strategies
    - Evaluate them using `$ ./manage.py evaluate_ai`

## Definitions
**Game**: A play through of multiple rounds starting with a fresh deck. A game ends when the deck runs out or the player
runs out of money

**Round**: A play starting from placing a single bet to finishing the hand as well as all split hands.
