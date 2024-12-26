from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib


app = Flask(__name__)
app.secret_key = 'yosa0516'


def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            grade TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# 获取学生信息（支持模糊查询）
def get_students(name=None, grade=None, age=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = "SELECT * FROM students WHERE 1=1"
    
    params = []
    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")
    if grade:
        query += " AND grade LIKE ?"
        params.append(f"%{grade}%")
    if age:
        query += " AND age = ?"
        params.append(age)
    
    cursor.execute(query, params)
    students = cursor.fetchall()
    conn.close()
    return students


# 获取用户信息（支持模糊查询）
def get_users(username=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = 'SELECT * FROM users WHERE 1=1'
    params = []

    if username:
        query += ' AND username LIKE ?'
        params.append(f'%{username}%')

    cursor.execute(query, tuple(params))
    users = cursor.fetchall()
    conn.close()
    return users


# 添加学生到数据库
def add_student(name, age, grade):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name, age, grade) VALUES (?, ?, ?)', (name, age, grade))
    conn.commit()
    conn.close()


# 更新学生信息
def update_student(student_id, name, age, grade):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE students SET name = ?, age = ?, grade = ? WHERE id = ?', (name, age, grade, student_id))
    conn.commit()
    conn.close()


# 删除学生
def delete_student(student_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()


# 添加用户（注册）
def add_user(username, password, is_admin=0):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', (username, password, is_admin))
    conn.commit()
    conn.close()


# 更新用户信息
def update_user(user_id, username, password, is_admin):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        if password:
            cursor.execute('UPDATE users SET username = ?, password = ?, is_admin = ? WHERE id = ?',
                            (username, password, is_admin, user_id))
        else:
            cursor.execute('UPDATE users SET username = ?, is_admin = ? WHERE id = ?',
                            (username, is_admin, user_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating user: {e}")
        conn.rollback()
    finally:
        conn.close()


# 删除用户
def delete_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()


# 定义根路由，返回页面为登录页面
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


# 定义登录路由，返回页面为登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['username'] = user[1]
            session['is_admin'] = user[3]
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


# 定义注册路由，返回页面为注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        is_admin = 0
        try:
            add_user(username, password, is_admin)
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists')
    return render_template('register.html')


# 定义仪表盘路由，返回页面为仪表盘页面
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    name = request.args.get('name')
    grade = request.args.get('grade')
    age = request.args.get('age')

    # 将查询条件传给 get_students 函数
    students = get_students(name=name, grade=grade, age=age)
    return render_template('dashboard.html', username=session['username'], is_admin=session['is_admin'], students=students)



# 定义管理员面板路由，返回页面为管理员面板页面
@app.route('/admin-panel', methods=['GET', 'POST'])
def admin_panel():
    if 'username' not in session or not session.get('is_admin'):
        return redirect(url_for('dashboard'))
    
    username = request.args.get('username', '')
    
    users = get_users(username)
    return render_template('admin_panel.html', username=session['username'], users=users)


# 定义添加学生路由，返回页面为仪表盘页面
@app.route('/add-student', methods=['POST'])
def add_student_route():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not session.get('is_admin'):
        return redirect(url_for('dashboard'))
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']
    add_student(name, age, grade)
    return redirect(url_for('dashboard'))


# 定义更新学生路由，返回页面为仪表盘页面
@app.route('/update-student/<int:student_id>', methods=['POST'])
def update_student_route(student_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    if not session.get('is_admin'):
        return redirect(url_for('dashboard'))
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']
    update_student(student_id, name, age, grade)
    return redirect(url_for('dashboard'))


# 定义删除学生路由，返回页面为仪表盘页面
@app.route('/delete-student/<int:student_id>', methods=['GET'])
def delete_student_route(student_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    if not session.get('is_admin'):
        return redirect(url_for('dashboard'))
    delete_student(student_id)
    return redirect(url_for('dashboard'))


# 定义更新用户路由，返回页面为管理员面板页面
@app.route('/update-user/<int:user_id>', methods=['POST'])
def update_user_route(user_id):
    if 'username' not in session or not session.get('is_admin'):
        return redirect(url_for('dashboard'))
    
    username = request.form['username']
    password = request.form.get('password')
    is_admin = 1 if 'is_admin' in request.form else 0

    try:
        if password:
            password = hashlib.sha256(password.encode()).hexdigest()
            update_user(user_id, username, password, is_admin)
        else:
            update_user(user_id, username, None, is_admin)
        return redirect(url_for('admin_panel'))
    except Exception as e:
        print(f"Error in update_user_route: {e}")
        flash('Error updating user. Please try again.')
        return redirect(url_for('admin_panel'))


# 定义删除用户路由，返回页面为管理员面板页面
@app.route('/delete-user/<int:user_id>', methods=['GET'])
def delete_user_route(user_id):
    if 'username' not in session or not session.get('is_admin'):
        return redirect(url_for('dashboard'))
    delete_user(user_id)
    return redirect(url_for('admin_panel'))


# 定义退出登录路由，返回页面为登录页面
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
    # 在同一局域网下开放端口，可以用 http://ip:5000 访问
    # 如果只需要对自己（127.0.0.1）开放，改成app.run()即可
