# -*- coding: utf-8 -*-
#
# Copyright 2011 Tobias Rodäbel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Silly Swarm is a simple multiplayer game using Web Sockets."""

from django.utils import simplejson
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from typhoonae import websocket
from uuid import uuid4 as UUID
import logging
import os


# Successfully completed handshake
HANDSHAKE_RECEIVED = 1

# A player made a move
PLAYER_MOVED = 2

# A player left the game
PLAYER_LEFT = 3

# Key name for keeping track of online players
PLAYERS_INDEX_KEY = "players"


class MainHandler(webapp.RequestHandler):
    """The main handler."""

    def get(self):
        """Creates a Web Socket URL and renders the index template."""

        websocket_url = websocket.create_websocket_url('/%s' % UUID())
        template_path = os.path.join(os.path.dirname(__file__), "index.html")
        self.response.out.write(template.render(template_path, locals()))


class HandshakeHandler(webapp.RequestHandler):
    """Handles Web Socket handshake requests."""

    def post(self, path):
        """Sends the HANDSHAKE_RECEIVED state to the particular user."""

        message = websocket.Message(self.request.POST)

        players = memcache.get(PLAYERS_INDEX_KEY)

        present_players = []

        if players:
            present_players = players[:]
            players.append(path)
            memcache.replace(PLAYERS_INDEX_KEY, players)
        else:
            players = [path]
            memcache.set(PLAYERS_INDEX_KEY, players)

        memcache.set(path, [])

        response = {'state': HANDSHAKE_RECEIVED, 'player': path}
        websocket.send_message([message.socket], simplejson.dumps(response))

        player_data = memcache.get_multi(present_players)

        for player in player_data:
            if not player_data[player]:
                continue

            x, y = player_data[player]
            response = {'state': PLAYER_MOVED, 'player': player, 'x': x, 'y': y}

            websocket.send_message([message.socket], simplejson.dumps(response))


class MessageHandler(webapp.RequestHandler):
    """Handles Web Socket messages."""

    def post(self, path):
        """Broadcasts all moves."""

        message = websocket.Message(self.request.POST)

        data = simplejson.loads(message.body)

        state = data.get("state")
        x = data.get('x')
        y = data.get('y')

        players = memcache.get(PLAYERS_INDEX_KEY) or []

        if state == PLAYER_MOVED:
            replace = {path: [x, y]}

            if path not in players:
                players.append()
                replace[PLAYERS_INDEX_KEY] = players

            memcache.replace_multi(replace)
            response = {'state': PLAYER_MOVED, 'player': path, 'x': x, 'y': y}

        elif state == PLAYER_LEFT or not data:
            memcache.delete(path)

            if path in players:
                players.remove(path)
                memcache.replace(PLAYERS_INDEX_KEY, players)

            response = {'state': PLAYER_LEFT, 'player': path}

        websocket.broadcast_message(simplejson.dumps(response))


class KillallHandler(webapp.RequestHandler):
    """Handler to kill all players at once."""

    def get(self):

        players = memcache.get(PLAYERS_INDEX_KEY) or []

        for player in players:
            response = {'state': PLAYER_LEFT, 'player': player}
            websocket.broadcast_message(simplejson.dumps(response))
            memcache.delete(player)
            players.remove(player)

        memcache.delete(PLAYERS_INDEX_KEY)


app = webapp.WSGIApplication([
    ('/', MainHandler),
    ('/_ah/websocket/handshake/(.*)', HandshakeHandler),
    ('/_ah/websocket/message/(.*)', MessageHandler),
    ('/killall', KillallHandler),
], debug=True)


def main():
    """The main function."""

    webapp.util.run_wsgi_app(app)


if __name__ == '__main__':
    main()
