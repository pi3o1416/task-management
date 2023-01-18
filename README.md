<h1>Task Management System</h1>

<h2>Overview</h2>
<p>This task management system is a Django project designed to help institutes and departments manage and track their tasks and goals. It includes features such as:</p>
<ul>
    <li>JWT authentication for secure user login</li>
    <li>Email verification for new users</li>
    <li>Admin panel for managing institutes, departments, and department members</li>
    <li>Permission handling for user authorization</li>
    <li>Setting of yearly and trek goals, and tracking of goal achievement</li>
    <li>Create, edit, delete, and view tasks</li>
    <li>Assign tasks to department members</li>
    <li>Generate employee monthly report of total task completions</li>
</ul>

<h2>Getting Started</h2>
<h3>Prerequisites</h3>
<ul>
    <li>Python 3.x</li>
    <li>Django 3.x</li>
    <li>Django REST framework</li>
    <li>Django Rest Framework JWT</li>
    <li>django-allauth</li>
    <li>PostgreSQL</li>
</ul>
<h3>Installation</h3>
<ol>
    <li>Clone the repository</li>
<pre>git clone https://github.com/your-username/task-management-system.git</pre>
    <li>Create a virtual environment and activate it</li>
    <pre>python -m venv env</pre>
    <pre>source env/bin/activate</pre>
    <li>Install dependencies</li>
    <pre>pip install -r requirements.txt</pre>
    <li>Create a .env file in the root directory with the following information:</li>
    <pre>
    SECRET_KEY=<your Django secret key>
    DEBUG=True
    DB_NAME=<your PostgreSQL database name>
    DB_USER=<your PostgreSQL database user>
    DB_PASSWORD=<your PostgreSQL database password>
    DB_HOST=<your PostgreSQL host>
    DB_PORT=<your PostgreSQL port>
    </pre>
    <li>Run migrations</li>
    <pre>python manage.py makemigrations</pre>
    <pre>python manage.py migrate</pre>
    <li>Create a superuser</li>
    <pre>python manage.py createsuperuser</pre>
    <li>Start the server</li>
    <pre>python manage.py runserver</pre>
</ol>
    <p>The system will be running on http://localhost:8000</p>

<h2>Usage</h2>
<ul>
    <li>Register as a new user and verify your email address</li>
    <li>Log in to the system </li>
    <li>If you are an admin, you can access the admin panel to manage institutes, departments, and department members.</li> 
    <li>Set your yearly and trek goals, and track your goal achievement</li> 
    <li>Create, edit, delete, and view tasks</li>
    <li>Assign tasks to department members</li>
    <li>Generate employee monthly report of total task completions</li>
</ul>


