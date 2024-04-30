# Purpose
This project, originally developed as part of CMPE 132, required us to create a fictious SJSU library called SJSUL where we would apply concepts that we learn throughout the course.

# Steps to run the App
> 1. Clone the repository<br>
Open your Linux terminal and execute the following command to clone the reporsitory:<br>
    `git clone https://github.com/Rodarkhen/cmpe132-project`

> 2. Create a Virtual Environment<br>
Before installing dependencies, it's a good practice to create a virtual environment to isolate the project's dependencies from other Python projects you may have.<br>
Use the following command to create a virtual environment named venv <br>
`python3 -m venv venv`<br>
This will set up a virtual environment in a directory named venv within your project directory.

> 3. Activate the Virtual Environment<br>
After creating the virtual environment, you need to activate it. This step ensures that when you install dependencies, they are isolated within this environment.<br>
`source venv/bin/activate`<br>
Once activated, you should see (venv) prefixed before your terminal prompt, indicating that the virtual environment is active.

> 4. Install Dependencies<br>
Now that the virtual environment is active, you can install the project dependencies listed in the dependencies.txt file.<br>
`pip3 install -r dependencies.txt`<br>
This command will install all the required dependencies specified in the dependencies.txt file.

> 5. Run the Application<br>
After installing the dependencies, you can run the application.<br>
`python3 run.py`<br>
This command will start the application on a local host.
