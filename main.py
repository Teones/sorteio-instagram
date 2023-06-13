from flask import Flask, render_template, request
from instagram_private_api import Client
import random
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    username = request.form['username']
    password = request.form['password']
    post_code = request.form['post_code']

    api = Client(username, password)

    post_id = None
    feed = api.self_feed()
    for item in feed['items']:
        if item['code'] == post_code:
            post_id = item['id']
            break

    users_valid_comments = []
    comments = api.media_n_comments(post_id, n=2000)
    for comment in comments:
        # match = re.findall(r"(@\w*)", comment['text'])
        # if len(match) >= 1 or True:
      users_valid_comments.append(comment['user_id'])

    random.shuffle(users_valid_comments)

    winners = set()
    i = 0
    while len(winners) < 1:
        if users_valid_comments[i] not in winners:
            winners.add(users_valid_comments[i])
        i += 1

    winner_ids = list(winners)
    winners_info = []
    for winner_id in winner_ids:
        winner = api.user_info(winner_id)['user']
        winners_info.append({
            'full_name': winner['full_name'],
            'username': winner['username']
        })

    return render_template('result.html', participants = len(users_valid_comments), winners=winners_info)

if __name__ == '__main__':
    app.run()