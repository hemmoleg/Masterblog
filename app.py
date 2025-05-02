import json

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)



@app.route('/')
def index():
    with open("posts.json", "r", encoding="utf-8") as posts:
        blog_posts = json.load(posts)
        print(posts)

    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=blog_posts)

# [
#     {"id": 1, "author": "John Doe", "title": "First Post", "content": "This is my first post."},
#     {"id": 2, "author": "Jane Doe", "title": "Second Post", "content": "This is another post."}
# ]

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        with open("posts.json", "r", encoding="utf-8") as posts:
            blog_posts = json.load(posts)

        post_id = blog_posts[len(blog_posts) - 1]['id']
        blog_posts.append({
            'author': author,
            'title': title,
            'content': content,
            'id': post_id + 1
        })
        with open("posts.json", "w", encoding="utf-8") as posts:
            json.dump(blog_posts, posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    with open("posts.json", "r", encoding="utf-8") as posts:
        blog_posts = json.load(posts)

    index_to_delete = next(
        (_idx for _idx, post in enumerate(blog_posts) if post['id'] == post_id),
        None
    )

    blog_posts.pop(index_to_delete)

    with open("posts.json", "w", encoding="utf-8") as f:
        json.dump(blog_posts, f)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    with open("posts.json", "r", encoding="utf-8") as posts:
        blog_posts = json.load(posts)

    post = next(
        (_post for _post in blog_posts if _post['id'] == post_id),
        None
    )

    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']

        # Save changes
        with open("posts.json", "w", encoding="utf-8") as f:
            json.dump(blog_posts, f)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

