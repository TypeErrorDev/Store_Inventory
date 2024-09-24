# How to create a virtual environment for your project
    
    -  Create a folder for your project
    -  Open your folder in your IDE
    -  Open the terminal in your IDE
    -  Install virtual environment
        -  Mac: python3 -m pip install --user virtualenv
        -  Windows: python -m pip install --user virtualenv
    -  Create a virtual environment
        -  Mac: python3 -m venv env
        Windows: python -m venv env
    Activate your environment
        Mac: source ./env/bin/activate
        Windows: .\env\Scripts\activate
    Install SQLAlchemy pip install sqlalchemy
    Create requirements file pip freeze > requirements.txt