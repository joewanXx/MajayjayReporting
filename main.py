from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
# A secret key is required to use sessions for tracking user login status.
# In a real application, this should be a complex, securely stored value.
app.secret_key = "kamoteng-kahoy-12345"

# --- Mock Data Moved from JavaScript to Python Backend ---
mock_user_db = {
    "admin@brgyportal.io": {"uid": "admin-uid-12345", "username": "admin", "password": "password", "role": "admin"},
    "user@brgyportal.io": {"uid": "user-uid-67890", "username": "user", "password": "password", "role": "resident"}
}

mock_reports = [
    {'id': 'R-1702588800000-1', 'reporter': 'Anonymous', 'title': 'Illegal Dumping Site', 'category': 'sanitation', 'location': 'Brgy. San Francisco, likod ng basketball court', 'description': 'Large piles of household trash and debris have accumulated over the past week.', 'status': 'New', 'date': '2025-10-13', 'response': None, 'proof': None},
    {'id': 'R-1702588800000-2', 'reporter': 'Yuan Gallardo', 'title': 'Lubak-lubak', 'category': 'infrastructure', 'location': 'Brgy. San Francisco, tapat ng petron', 'description': 'A deep pothole has formed, causing traffic issues and hazard to cyclists.', 'status': 'In Progress', 'date': '2025-10-12', 'response': 'Inspection complete. Work crew scheduled for repair on 10/18.', 'proof': 'RoadRepairPlan.pdf'},
    {'id': 'R-1702588800000-3', 'reporter': 'Rose Ann Mae Flores', 'title': 'Maingay na Chismosa', 'category': 'noise', 'location': 'St. Francis, Kamote Avenue', 'description': 'Noise levels exceed permitted hours, especially early in the morning (6 AM).', 'status': 'Resolved', 'date': '2025-10-10', 'response': 'Contractor warned and hours adjusted. Issue closed.', 'proof': 'ResolvedSitePhoto.jpg'},
    {'id': 'R-1702588800000-4', 'reporter': 'Johan Arsolacia', 'title': 'Nadulas ako Kanina', 'category': 'infrastructure', 'location': 'A. Luna Street, Brgy. San Francisco', 'description': 'Water is leaking severely, causing flooding on the street. Needs urgent attention.', 'status': 'New', 'date': '2025-10-14', 'response': None, 'proof': None},
]
# Security headers middleware
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self' https://fonts.googleapis.com https://cdnjs.cloudflare.com https://fonts.gstatic.com https://cdn.tailwindcss.com 'unsafe-inline' 'unsafe-eval'"
    return response

@app.route('/')
def home():
    # home page ng administrator
    if 'user' in session and session['user']['role'] == 'admin':
        return render_template('adminPage/admin_home.html', session=session)
    
    # pag hindi naka login as admin, home page ng resident
    return render_template('home.html', current_page='home', session=session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = f"{username.lower().strip()}@brgyportal.io"

        user = mock_user_db.get(email)

        if user and user['password'] == password:
            # Store user info in the session
            session['user'] = {
                'email': email,
                'uid': user['uid'],
                'role': user['role'],
                'username': user['username']
            }
            flash('Login successful! Welcome back.', 'success')
            if user['role'] == 'admin':
                return redirect(url_for('admin'))
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return redirect(url_for('login'))

    # For GET requests, just show the login page
    return render_template('auth/login.html', current_page='auth', session=session)

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    email = f"{username.lower().strip()}@brgyportal.io"

    if password != confirm_password:
        flash('Passwords do not match.', 'error')
        return redirect(url_for('login'))

    if email in mock_user_db:
        flash('This username is already taken.', 'error')
        return redirect(url_for('login'))

    # Create a new user (in a real app, you'd hash the password)
    new_user = {'uid': f'user-uid-{len(mock_user_db) + 1}', 'username': username, 'password': password, 'role': 'resident'}
    mock_user_db[email] = new_user

    flash('Account created successfully! Please log in.', 'success')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None) # Clear the user session
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/account')
def account():
    # Protect the route, only logged-in users can see it
    if 'user' not in session:
        flash('You need to be logged in to see your account page.', 'info')
        return redirect(url_for('login'))
    
    return render_template('userPage/account.html', current_page='account', session=session)

@app.route('/report')
def report():
    return render_template('userPage/submit_report.html', current_page='submit-report', session=session)

@app.route('/reports')
def reports():
    return render_template('publicRep/view_reports.html', current_page='view-reports', session=session, reports=mock_reports)

@app.route('/admin')
def admin():
    # A simple protection for the admin route
    if 'user' not in session or session['user']['role'] != 'admin':
        flash('You must be an administrator to access this page.', 'error')
        return redirect(url_for('login'))
    
    # Pass the reports and user data to the template for rendering
    return render_template(
        'adminPage/admin_dashboard.html', 
        current_page='admin-dashboard', 
        session=session, 
        reports=mock_reports, 
        users=mock_user_db)

@app.route('/admin/update_report', methods=['POST'])
def update_report():
    # Ensure an admin is logged in
    if 'user' not in session or session['user']['role'] != 'admin':
        flash('Unauthorized action.', 'error')
        return redirect(url_for('login'))

    report_id = request.form.get('report_id')
    new_status = request.form.get('status')
    new_response = request.form.get('response')

    # Find the report in our mock data
    report_to_update = next((report for report in mock_reports if report['id'] == report_id), None)

    if report_to_update:
        report_to_update['status'] = new_status
        report_to_update['response'] = new_response
        flash(f"Report '{report_id}' has been updated successfully.", 'success')
    else:
        flash(f"Error: Report with ID '{report_id}' not found.", 'error')
    
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)