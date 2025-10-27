from flask import Flask,make_response
from http import HTTPStatus

# Initialize the Flask application
app = Flask(__name__)

# --- Configuration ---
# You define the application version directly in the code.
# You will change this string later to test the CI/CD pipeline.
APP_VERSION = "v1.0.1"

# --- Routes ---

@app.route('/')
def hello():
    """
    Returns a simple greeting with the application version.
    This is the main endpoint of the application.
    """
    return f"Hello from {APP_VERSION}"

@app.route('/healthz')
def healthz():
    """
    Health check endpoint.
    Returns a 200 OK status to indicate that the application is running and healthy.
    This is used by Kubernetes for liveness and readiness probes.
    """
    return str(HTTPStatus.OK.value),HTTPStatus.OK
@app.route('/version')
def healthz():
    return f"{APP_VERSION}"



if __name__ == '__main__':
    # Run the app on host 0.0.0.0 to be accessible from outside the container
    app.run(host='0.0.0.0', port=5000)