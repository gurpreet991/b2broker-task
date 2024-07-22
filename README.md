# b2broker-task

## Prerequisites

Ensure you have the following installed on your system:
- Python 3.x
- pip (Python package installer)
- virtualenv (optional but recommended)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/b2broker-task.git
    cd b2broker-task
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the project dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

7. **Access the application:**

    Open your web browser and go to `http://127.0.0.1:8000/`


