from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import Travel, User, Database
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash

travel_controller = Blueprint('travel_controller', __name__)
auth = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@travel_controller.route('/dashboard')
@login_required
def dashboard():
    travels, _, total = Travel.get_all_travels(count_all=True)
    
    if not travels:
        total_travels = 0
        total_cost = 0
        unique_places = 0
    else:
        total_travels = total
        total_cost = sum(travel[4] for travel in travels)
        unique_places = len(set(travel[1] for travel in travels if travel[5] == 5))
    
    return render_template('dashboard.html',
                         total_travels=total_travels,
                         total_cost=total_cost,
                         unique_places=unique_places)

@travel_controller.route('/travels')
@login_required
def index():
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 6  
    
    travels, total_pages, total_items = Travel.get_all_travels(
        search=search, 
        page=page, 
        per_page=per_page
    )
  
    def get_page_range(current, total):
        start = max(1, current - 2)
        end = min(total + 1, current + 3)
        return range(start, end)
    
    return render_template('index.html',
                         travels=travels,
                         search=search,
                         current_page=page,
                         total_pages=total_pages,
                         total_items=total_items,
                         page_range=get_page_range(page, total_pages))

@travel_controller.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        try:
            travel = Travel(
                place_name=request.form['place_name'],
                description=request.form['description'],
                travel_date=datetime.strptime(request.form['travel_date'], '%Y-%m-%d'),
                cost=float(request.form['cost']),
                rating=int(request.form.get('rating', 3)),
                username=session['user_id']
            )
            Travel.create_travel(travel)
            return redirect(url_for('travel_controller.index'))
        except Exception as e:
            print(f"Error creating travel: {e}")
            return "Error creating travel entry", 500
    
    return render_template('create.html')

@travel_controller.route('/update/<int:travel_id>', methods=['GET', 'POST'])
@login_required
def update(travel_id):
    if request.method == 'POST':
        try:
            travel = Travel(
                place_name=request.form['place_name'],
                description=request.form['description'],
                travel_date=datetime.strptime(request.form['travel_date'], '%Y-%m-%d'),
                cost=float(request.form['cost']),
                rating=int(request.form.get('rating', 3)),
                username=session['user_id']
            )
            Travel.update_travel(travel_id, travel)
            return redirect(url_for('travel_controller.index'))
        except Exception as e:
            print(f"Error updating travel: {e}")
            return "Error updating travel entry", 500
    
    travel = Travel.get_travel(travel_id)
    if not travel:
        return "Travel not found", 404
    
    return render_template('update.html', travel=travel)

@travel_controller.route('/delete/<int:travel_id>', methods=['POST'])
@login_required
def delete(travel_id):
    try:
        Travel.delete_travel(travel_id)
        return redirect(url_for('travel_controller.index'))
    except Exception as e:
        print(f"Error deleting travel: {e}")
        return "Error deleting travel entry", 500

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.check_user(username, password):
            session['user_id'] = username
            return redirect(url_for('travel_controller.dashboard'))
        flash('Username atau password salah!')
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Password tidak cocok!')
            return render_template('register.html')
        
        try:
            User.create_user(username, password)
            return redirect(url_for('auth.login'))
        except:
            flash('Username sudah digunakan!')
    
    return render_template('register.html')

@auth.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            flash('Password baru tidak cocok!')
            return render_template('forgotpassword.html')
        
        try:
            db = Database()
            db.cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user = db.cursor.fetchone()
            if user:
                hashed_password = generate_password_hash(new_password)
                db.cursor.execute(
                    "UPDATE users SET password = %s WHERE username = %s",
                    (hashed_password, username)
                )
                db.connection.commit()
                flash('Password berhasil direset!')
                return redirect(url_for('auth.login'))
            else:
                flash('Username tidak ditemukan!')
            db.close()
        except Exception as e:
            flash('Terjadi kesalahan!')
            print(e)
    
    return render_template('forgotpassword.html')