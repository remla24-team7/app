# app

This is the repository for the app of Assigment 2. 

The frontend is in the `frontend` folder and the backend is just `app.py`. 

Entering a URL and clicking "Predict" in the web frontend queries the `app-service` backend, which then communicates with `model-service` to retrieve the prediction. The prediciton is then shown on the website. Make sure to have `model-service` running and configured (`MODEL_SERVICE_URL`) for this backend to work.

## Specifications

* Displays lib-version information through first installing packaage through poetry and then using its version query functionality. 
* Communicates to model-service via REST.
* URL of model-service is configurable through environment variable

## Application version two

This branch contains the version 2 of the application used for experimentation. This version has the same functionality as the base version, but now has some css for styling and added descriptions to allow for smoother navigation of the website. 