from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Function to connect to the database and create our table if it doesn't exist yet
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Create a table for posts with an automatic ID, Title, and Content columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Route to display the feed from the database
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Fetch all posts from oldest to newest (or reverse it by adding DESC)
    cursor.execute('SELECT title, content FROM posts ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    
    # Convert database rows into a clean dictionary format for our HTML page
    posts_db = [{"title": row[0], "content": row[1]} for row in rows]
    
    return render_template('index.html', posts=posts_db)

# Route to process and insert a new user post into the database
@app.route('/create-post', methods=['POST'])
def create_post():
    title = request.form.get('title')
    content = request.form.get('content')
    
    if title and content:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        # Securely insert the data into our table rows
        cursor.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        
    return redirect('/')

if __name__ == '__main__':
    init_db() # Run the database builder when the app starts up
    app.run(debug=True, host='0.0.0.0', port=5001)