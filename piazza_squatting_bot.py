from piazza_api import Piazza
import time
import requests
import json
import sys
import yaml
from pypandoc import convert_text

webhook_url = ''
classes = []


class PiazzaClass:
    '''
    Represents a class on Piazza.
    '''

    def __init__(self, name, network, network_id,
                 subscribers, icon_emoji, bot_name):
        '''(str, piazza_api.Network, list[str], str, str)
        Create a new Piazza Class with the given class name, network id, list
        of Slack handles to receive notifications, bot emoji and bot name.
        '''
        self.name = name
        self.network = network
        self.network_id = network_id
        self.subscribers = subscribers
        self.icon_emoji = icon_emoji
        self.bot_name = bot_name
        self.last_notified_post = None

    def notify(self, subject, question_url, body):
        '''
        Notify's this classe's subscribers with the given subject, a link to the
        given question url, and question body.
        '''
        subscriber_mentions = ' '.join(['<@%s>' % s for s in self.subscribers]
        requests.post(webhook_url, {'payload': json.dumps({
            'channel': '#general',
            'username': self.bot_name,
            'icon_emoji': self.icon_emoji,
            'text': '%s New post in %s Piazza' %
                    (subscriber_mentions, self.name),
            'attachments': [{
                "title": subject,
                "title_link": question_url,
                "text": body,
            }],
        })})


def get_config():
    '''
    Reads, parses and returns a dictionary containing the contents of
    config.yml
    '''
    try:
        config_file=open('config.yml', 'r')
        yaml_config=yaml.load(config_file)
        config_file.close()
    except IOError:
        sys.exit('config.yml was not found or error parsing YAML')

    return yaml_config


def parse_class_configs(piazza):
    '''
    Initializes the bot with the class configs found in config.yml and sets
    the global webhook_url. Needs a Piazza object to get the network object
    for each class.
    '''
    yaml_config=get_config()

    for config in yaml_config['class_configs']:
        network=piazza.network(config['network_id'])
        classes.append(
            PiazzaClass(
                config['name'],
                network,
                config['network_id'],
                config['subscribers'],
                config['icon_emoji'],
                config['bot_name']))


def parse_global_config():
    '''
    Parses and sets global (ie. not related to a particular class) configuration
    data from config.yml
    '''
    yaml_config=get_config()
    global webhook_url
    webhook_url=yaml_config['webhook_url']


def try_login():
    '''
    Tries to login to Piazza using the username/password specified in config.yml
    '''
    yaml_config=get_config()

    print 'Attempting to login to Piazza as %s.....' % yaml_config['username'],
    piazza=Piazza()

    try:
        piazza.user_login(
            email=yaml_config['username'], password=yaml_config['password'])
    except BaseException:
        print 'failed, check username/password'

    print 'success'
    return piazza


def announce_online():
    '''
    Sends a message to #general stating the bot is starting
    '''
    requests.post(webhook_url, {'payload': json.dumps({
        'channel': '#general',
        'text': 'Piazza squatting bot is starting. Monitoring classes: %s' %
                ', '.join([cl.name for cl in classes])
    })})


def poll_classes():
    '''
    Loops until program is terminated, polling Piazza periodically for new posts
    and notifying all subscribers of that class.
    '''
    while True:
        for cl in classes:
            # No latest post yet (bot has just started), set top post as latest
            if cl.last_notified_post is None:
                latest_post_in_class=next(cl.network.iter_all_posts(limit=1))
                cl.last_notified_post=latest_post_in_class['nr']
                continue

            # Grab all new posts
            to_notify=[]
            for post in cl.network.iter_all_posts(limit=5):
                if post['bucket_name'] == 'Pinned':
                    continue

                if post['nr'] > cl.last_notified_post:
                    to_notify.append(post)

            # Send a notification for each one and update cl.last_notified_post
            for post in to_notify:
                question_url='https://piazza.com/class/%s?cid=%s' % (
                    cl.network_id, post['nr'])

                # 0xA0 = Non breaking space, found in Piazza HTML, must be
                # converted to regular space
                subject=convert_text(post['history'][0]['subject'].replace(
                    u'\xa0', ' '), 'plain', format='html')
                body=convert_text(post['history'][0]['content'].replace(
                    u'\xa0', ' '), 'plain', format='html')
                cl.notify(subject, question_url, body)

                if cl.last_notified_post < post['nr']:
                    cl.last_notified_post=post['nr']

        time.sleep(10)


piazza=try_login()
parse_global_config()
parse_class_configs(piazza)
announce_online()

try:
    poll_classes()
except KeyboardInterrupt:
    sys.exit('Caught KeyboardInterrupt')
except BaseException:
    import traceback
    traceback.print_exc()
    print 'Unknown error occured'
