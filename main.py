from werkzeug.serving import run_simple

from microservice.main import application

# Well, you can run the app even without Gunicorn.
if __name__ == '__main__':
    run_simple('localhost', 4000, application)
