from flask import Flask, render_template, request, redirect, url_for
from models import db, User, Profile

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        location = request.form.get('location')
        results = Profile.query.filter_by(location=location).all()
        return render_template('search.html', results=results)
    return render_template('search.html')

@app.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        age = request.form.get('age')
        fitness_goals = request.form.get('fitness_goals')
        location = request.form.get('location')
        workout_preferences = request.form.get('workout_preferences')

        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()

        profile = Profile(user_id=user.id, age=age, fitness_goals=fitness_goals, location=location, workout_preferences=workout_preferences)
        db.session.add(profile)
        db.session.commit()

        
        return redirect(url_for('profile', user_id=user.id))
    return render_template('create_profile.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)