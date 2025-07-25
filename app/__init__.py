import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import datetime
from peewee import *
from playhouse.shortcuts import model_to_dict

load_dotenv()

app = Flask(__name__)
if os.getenv('TESTING') == 'true':
    print('Running in test mode')
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306,
)
print(mydb)
print(os.getenv("MYSQL_DATABASE"))

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


import time
from peewee import OperationalError

max_retries = 10
for attempt in range(max_retries):
    try:
        mydb.connect()
        print("Connected to MySQL")
        break
    except OperationalError as e:
        print(f"Attempt {attempt+1} failed: {e}")
        time.sleep(3)
else:
    raise Exception("Could not connect to MySQL after several attempts")

mydb.connect()
mydb.create_tables([TimelinePost])


@app.route('/')
def index():
    return render_template(
        'about.html',
        title="About",
        url=os.getenv("URL"),
        name="Arbab",
        about_text=(
            "A student at The City College of New York studying computer science. "
            "I am currently building full-stack web applications using React and Python frameworks. "
            "Recently, I have begun exploring AI and integrating its features within my projects to serve specific purposes. "
            "Additionally, I have started venturing beyond web development, beginning with site reliability engineering (SRE). "
            "Outside of programming, my passions include sports and fitness. I'm a huge soccer fan and have loved the game since I was a kid. "
            "I'm also getting into calisthenics to lead a healthier future."
        ),
        skills=["React", "Python", "JavaScript", "Flask", "REST APIs"],
        hobbies=["Soccer", "Calisthenics", "TV Shows", "Gaming"]
    )

@app.route('/about')
def about():
    return render_template(
        'about.html',
        title="About",
        url=os.getenv("URL"),
        name="Arbab",
        about_text=(
            "A student at The City College of New York studying computer science. "
            "I am currently building full-stack web applications using React and Python frameworks. "
            "Recently, I have begun exploring AI and integrating its features within my projects to serve specific purposes. "
            "Additionally, I have started venturing beyond web development, beginning with site reliability engineering (SRE). "
            "Outside of programming, my passions include sports and fitness. I'm a huge soccer fan and have loved the game since I was a kid. "
            "I'm also getting into calisthenics to lead a healthier future."
        ),
        skills=["React", "Python", "JavaScript", "Flask", "REST APIs"],
        hobbies=["Soccer", "Calisthenics", "TV Shows", "Gaming"]
    )


@app.route('/hobbies')
def hobbies():
    return render_template(
        'hobbies.html',
        title="Hobbies",
        url=os.getenv("URL"),
        hobbies=[
            {
                "icon": "⚽",
                "name": "Soccer",
                "description": (
                    "I've been passionate about soccer since I was a kid. "
                    "My favorite team is FC Barcelona and my all time favorite player is Andres Iniesta. "
                    "I set aside time to play soccer with my friends almost every week."
                )
            },
            {
                "icon": "🏋️",
                "name": "Calisthenics",
                "description": (
                    "Training with my bodyweight helps me build strength and discipline. "
                    "I also enjoy working out outdoors in jungle gyms just because it doesn't feel suffocating. "
                    "I'm currently in the midst of recovering from some shoulder injuries and slowly working back up to my normal routine."
                )
            },
            {
                "icon": "📺",
                "name": "Binging TV Shows and Movies",
                "description": (
                    "I unwind with shows every night. I mostly enjoy thrillers but I have recently started exploring other genres."
                )
            },
            {
                "icon": "🎧",
                "name": "Music & Podcasts",
                "description": (
                    "Whether I'm working out, coding, or walking, I always have a playlist or podcast running in the background."
                )
            }
        ]
    )


@app.route('/experiences')
def experiences():
    return render_template(
        'experiences.html',
        title="Experiences",
        url=os.getenv("URL"),
        experiences=[
            {
                "title": "SRE Fellow",
                "company": "Meta x MLH",
                "duration": "June 2025 – Present",
                "bullets": [
                    "Incoming Meta x MLH site reliability fellow"
                ]
            },
            {
                "title": "Software Engineer Intern",
                "company": "IT Services LLC",
                "duration": "July 2024 – August 2024",
                "bullets": [
                    "Led development of an AI chatbot using Groq API with Llama 3.1, tailored for K-12 math tutoring.",
                    "Integrated GTTS for text-to-speech with 5 voices and 3 accents, enhancing accessibility for users.",
                    "Worked on backend integration with MongoDB and REST APIs to store and retrieve chat history efficiently."
                ]
            },
            {
                "title": "Computer Aide Intern",
                "company": "Con Edison",
                "duration": "Dec 2022 – May 2025",
                "bullets": [
                    "Coordinated and assigned over 5,000 CM/PM work orders using IBM Maximo, ensuring alignment with scope and unit outages.",
                    "Optimized complex SQL queries in Maximo to extract and analyze 100K+ records, improving planning and decision-making.",
                    "Built a custom Power App with Power Automate to send automated emails, cutting processing time by 20%.",
                    "Automated Excel data tasks with VBA, reducing manual work by 75% and significantly boosting accuracy."
                ]
            }
        ]
    )


@app.route('/education')
def education():
    return render_template(
        'education.html',
        title="Education",
        url=os.getenv("URL"),
        school={
            "name": "City College of New York (CUNY)",
            "degree": "B.S. in Computer Science",
            "duration": "Expected Dec 2025",
            "description": (
                "Currently pursuing a Bachelor's in Computer Science, focusing on "
                "software engineering, systems programming, and artificial intelligence."
            )
        },
        coursework=[
            "Data Structures & Algorithms",
            "Operating Systems",
            "Software Engineering",
            "Artificial Intelligence",
            "Database Systems",
            "Computer Architecture"
        ]
    )

@app.route("/timeline")
def timeline():
    return render_template('timeline.html', title="Timeline")

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']

    # Validate required fields
    if not name:
        return "Invalid name", 400
    
    if not content:
        return "Invalid content", 400
    
    if not email or '@' not in email or '.' not in email:
        return "Invalid email", 400
    
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]
        }

@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_time_line_post(post_id):
    post = TimelinePost.get_by_id(post_id)
    post.delete_instance()
    return model_to_dict(post)


