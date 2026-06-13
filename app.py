from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Simulated in-memory database to hold user posts
posts_db = [
    {"title": "Welcome to the Platform!", "content": "This is the very first post on our full-stack content platform."},
    {"title": "Learning Full-Stack Development", "content": "Building APIs with Flask makes data communication simple."}
]

# Route to display the feed and the submission form
@app.route('/')
def home():
    return render_template('index.html', posts=posts_db)

# Route to process and add a new user post
@app.route('/create-post', methods=['POST'])
def create_post():
    title = request.form.get('title')
    content = request.form.get('content')
    
    if title and content:
        # Append the new post to our database list
        posts_db.insert(0, {"title": title, "content": content})
        
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Using port 5001 so it doesn't conflict with your first app