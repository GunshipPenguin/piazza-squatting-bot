from piazza_api import Piazza
import time
import requests
import json
import argparse
from pypandoc import convert_text

# Email/Password to login to Piazza with
EMAIL = ''
PASSWORD = ''

# Slack webhook URL for notifications
WEBHOOK_URL = ''

# Piazza class name and network ID
CLASS_NAME = ''
NETWORK_ID = ''

# Bot name and emoji to use as bot icon
BOT_NAME = ''
ICON_EMOJI = ''

while True:
    print 'Logging into Piazza...'
    try:
        p = Piazza()
        p.user_login(email=EMAIL, password=PASSWORD)

        requests.post(WEBHOOK_URL, {'payload': json.dumps({
            'channel': '#general',
            'username': BOT_NAME,
            'text': '%s is starting' % BOT_NAME,
            'icon_emoji': ICON_EMOJI,
            'link_names': True
        })})

        n = p.network(NETWORK_ID)

        latest_post = None
        next_latest_post = None

        while True:
            for post in n.iter_all_posts(limit=5):
                if post['bucket_name'] == 'Pinned':
                    continue
                nr = post['nr']
                print nr, latest_post
                if latest_post is None:
                    next_latest_post = nr
                    break
                if nr > latest_post:
                    question_url = 'https://piazza.com/class/%s?cid=%s' % (
                        NETWORK_ID, nr)
                    subject = convert_text(post['history'][0]['subject'].replace(
                        u'\xa0', ' '), 'markdown', format='html')
                    body = convert_text(post['history'][0]['content'].replace(
                        u'\xa0', ' '), 'markdown', format='html')
                    requests.post(WEBHOOK_URL, {'payload': json.dumps({
                        'channel': '#general',
                        'username': BOT_NAME,
                                    'text': '@channel New post in %s :crystal_ball: :crystal_ball: :crystal_ball:' % CLASS_NAME,
                                    'attachments': [{
                                        "fallback": 'New post in %s: %s' % (CLASS_NAME, question_url),
                                        "title": subject,
                                        "title_link": question_url,
                                        "text": body,
                                        "mrkdwn_in": ["text"]
                                    }],
                        'icon_emoji': ICON_EMOJI,
                        'link_names': True
                    })})
                    next_latest_post = max(next_latest_post, nr)

            latest_post = next_latest_post
            time.sleep(10)
    except KeyboardInterrupt:
        break
    except:
        import traceback
        traceback.print_exc()
        print 'Restarting app...'
