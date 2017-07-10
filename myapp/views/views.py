from . import app

@app.route('/r/<list:subreddits>')
def subreddit_home(subreddits):
    """显示给定subreddits里的所有帖子"""
    posts = []
    for subreddit in subreddits:
        posts.extend(subreddit.posts)

    return render_template('/r/index.html', posts=posts)