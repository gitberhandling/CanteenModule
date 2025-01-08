# Canteen Ease: Canteen Ordering System  

Canteen Ease is a Python-based software solution designed to simplify and enhance the dining experience for students in educational institutions. This project streamlines meal ordering, tracking, and management, making the process efficient and user-friendly.  

---

## Features  
- Simplified meal ordering and tracking  
- Efficient management of cafeteria services  
- User-friendly graphical interface  

---

## How to Run the Project  

Follow these steps to get started:  

1. Clone the repository:  
   ```bash
   git clone https://github.com/gitberhandling/CanteenModule.git
   cd CanteenModule
2. Set up a virtual environment (optional):

   For Linux/MacOS:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate

   For Windows:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   
4. Set up the MySQL database:
Create a new MySQL database for the project.
Update the database connection details (host, user, password, database) in the canteen.py file.

5. Run the application:

   ```bash
   python canteen.py
