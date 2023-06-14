from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from instagram_private_api import Client
import random
import re

@csrf_exempt
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def result(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        post_code = request.POST.get('post_code')

        pattern = r'/p/([A-Za-z0-9_-]+)/'
        code = re.search(pattern, post_code)
        if code:
            post_code = code.group(1)
            
        # Lógica de processamento dos dados
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
            # if len(match) >= 1:
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

        return render(request, 'result.html', {'participants': len(users_valid_comments), 'winners': winners_info})

    return render(request, 'result.html')
