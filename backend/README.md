# LinkedIn Job Scraper Backend

## Development Setup

### Option 1: Using Docker (Recommended)

1. Install Docker and Docker Compose on your machine:

   - [Docker Desktop for Mac/Windows](https://www.docker.com/products/docker-desktop)
   - [Docker Engine for Linux](https://docs.docker.com/engine/install/)

2. Clone the repository and navigate to the backend folder:
   - Ensure you have Python 3.6 or higher installed. [Download Python here](https://www.python.org/downloads/).
   - Navigate to the `backend` folder using `cd backend`.
   - Create a virtual environment with `python3 -m venv venv`.
   - Activate the virtual environment using `source venv/bin/activate` on Mac/Linux or `venv\Scripts\activate` on Windows.
   - Install the required dependencies with `pip install -r requirements.txt`.
   - Run the Flask development server using `python run.py`.
   - When finished, deactivate the virtual environment by running `deactivate`.

# Save dependencies to requirements.txt

`pip freeze > requirements.txt`

# Rebuild Docker container when requirements change

If you've updated the requirements.txt file, rebuild the Docker container:

`docker-compose build --no-cache`
