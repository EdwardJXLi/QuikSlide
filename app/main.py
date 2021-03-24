from flask import Flask, render_template, send_from_directory, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required

from app.models.user import User
from app.models.project import Project
from app.db import db
from app.process.process import Process
import os
# from transformers import pipeline

app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(os.path.join(project_dir, "dev.db"))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

raise NotImplementedError("Fill In The App Credentials Here!!!")
app.config['SECRET_KEY'] = None
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
# summarizer = pipeline("summarization")

from app.views import login

@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/transformers")
# def transformers():
#     ARTICLE = "Many scientists and researchers across the globe are working on understanding more about the virus to develop effective treatments which can include vaccines or drugs to reduce the severity of attack. Our knowledge on this topic keeps increasing. AI can help humans prioritize their time effectively if it can do a first pass of reading through the research and providing a good summary. However summarization tends to be a difficult and subjective task. To truly summarize AI needs to understand the content which is difficult due to the large variation in writing styles of researchers. In this blog we evaluate how well the BART Transformer model does in summarizing the content of COVID-19 papers."
#     return summarizer(ARTICLE, max_length=130, min_length=30)

@app.route("/testcrash")
def testcrash():
    raise Exception("Test Exception")

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    print("CREATE")
    if request.method == "POST":
        script = request.form["script"]
        title = request.form.get("title")

        if title.strip() == "":
            title = None

        slides = Process(script)
        slides.process(current_user.email, current_user.username, title)
        
        new_project = Project(owner=current_user.id, name=slides.name, link=slides.link)
        db.session.add(new_project)
        db.session.commit()

        return render_template("create.html", link=slides.link)
        
    return render_template("create.html")

@app.route("/dashboard")
@login_required
def dashboard():
    projects = Project.query.filter_by(owner=current_user.id).all()
    return render_template("dashboard.html", projects=projects)

@app.errorhandler(500)
def internal_error(error):
    return render_template("404.html")
