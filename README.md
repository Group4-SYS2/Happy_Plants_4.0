How to run the program:

  1. Create a python virtual environment:
     
     1.1 Windows: `python -m venv`
     
     1.2 MacOS: `python3 -m venv venv`
     
  2. Start the virtual environment:

     2.1 Windows: `venv/Scripts/activate`
     
     2.2 MacOS: `source venv/bin/activate`
    
  3. Download all the requirements: `pip install -r src/requirements.txt`
  4. Navigate to the server: `cd src/server`
  5. Start the program: `fastapi dev app.py`

You can now access the site through http://127.0.0.1:8000/

CI trigger
