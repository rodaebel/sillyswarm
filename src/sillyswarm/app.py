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
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from typhoonae import websocket
from uuid import uuid4 as UUID


# Successfully completed handshake
HANDSHAKE_RECEIVED = 1

# A player made a move
PLAYER_MOVED = 2

# A player left the game
PLAYER_LEFT = 3


class MainHandler(webapp.RequestHandler):
    """The main handler."""

    def get(self):
        """Creates a Web Socket URL and renders the index template."""

        websocket_url = websocket.create_websocket_url('/%s' % UUID())
        self.response.out.write(template.render('index.html', locals()))


class HandshakeHandler(webapp.RequestHandler):
    """Handles Web Socket handshake requests."""

    def post(self, path):
        """Sends the HANDSHAKE_RECEIVED state to the particular user."""

        message = websocket.Message(self.request.POST)

        response = {'state': HANDSHAKE_RECEIVED, 'player': path}
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

        if state == PLAYER_MOVED:
            response = {'state': PLAYER_MOVED, 'player': path, 'x': x, 'y': y}
        elif state == PLAYER_LEFT or not data:
            response = {'state': PLAYER_LEFT, 'player': path}

        websocket.broadcast_message(simplejson.dumps(response))


app = webapp.WSGIApplication([
    ('/', MainHandler),
    ('/_ah/websocket/handshake/(.*)', HandshakeHandler),
    ('/_ah/websocket/message/(.*)', MessageHandler),
], debug=True)


def main():
    """The main function."""

    webapp.util.run_wsgi_app(app)


if __name__ == '__main__':
    main()
