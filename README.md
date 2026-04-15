# Happy Plants 4.0

## About the Project

Happy Plants is an website designed to help users care for their indoor plants while providing them with information about those plants.  
It utilizes information retrieved from [Trefle.io](//Trefle.io), which is an open and free API offering data on over one million plant species and hybrids.  
Happy Plants features a colorful graphical user interface developed in Python, and allows users to search through tens of thousands of plants, name them, and add them to their personal library.  
The application also reminds the user when it is time to water, based on calculations done behind the scene.

##   
Requirements

*   Python 3.13
    
*   Dependencies listed in `requirements.txt`
    

## How to run the program:

1.  Create a python virtual environment:
    
    1.1 Windows: `python -m venv`
    
    1.2 MacOS: `python3 -m venv venv`
    
2.  Start the virtual environment:
    
    2.1 Windows: `venv/Scripts/activate`
    
    2.2 MacOS: `source venv/bin/activate`
    
3.  Download all the requirements: `pip install -r src/requirements.txt`
    
4.  Navigate to the server: `cd src/server`
    
5.  Start the program: `fastapi dev app.py`
    

You can now access the site through [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Link to Kanban board: [https://github.com/orgs/Group4-SYS2/projects/3/views/2](https://github.com/orgs/Group4-SYS2/projects/3/views/2)

## Contributors

These are the project contributors along with their main focus areas

*   priscilla-wettlen - Priscilla
    
    *   Creating the CI pipeline and adding plant filtering
        
*   christianglian - Christan
    
    *   Refactoring the backend-database communication
        
*   Menaanasir - Mena
    
    *   Writing tests and improving frontend-backend connections
        
*   Smalandaren - Isabelle
    
    *   Code management, cleanup and updating tests
        
*   Steffeman69 - Rasmus
    
    *   Adding multi-user handling and water status functionality
        
*   ahmadrules - Ahmad
    
    *   Setting up the project base