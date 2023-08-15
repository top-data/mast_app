# AI Package for Mastitis Application
This repository includes all the files, models and dependencies required for running AI models and returning the predictions.
- Expected Input: a csv file contains pre-processed data from one herd, e.g. herd tests, reproduction tests, etc.
- Expected output: a json file contains predicted likelihoods and cow qualities.

# AI Demo Web Application
- A basic app was built to demonstrate the AI block and is available at [https://mast-app.azurewebsites.net/](url).

# File Description
- app.py and templates: these files/folder along with main.py are used for a demo web app Only. I developed a basic demo app to make sure all the dependencies and the AI package working together without issue. The app is available at [https://mast-app.azurewebsites.net/](url)
- main.py: a few lines of code to show how to run the AI models and return the predictions.
- ai_functions: all the functions required for running the AI block.
- model_Outcome_...: AI models for different outcomes.
- requirements.txt: all the dependencies and packages requires for running the models
- Python version: Python 3.10.9
