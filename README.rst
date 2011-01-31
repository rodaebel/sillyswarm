===========
Silly Swarm
===========

Browser game to demonstrate TyphoonAE's Web Socket Service.


Copyright and License
---------------------

Copyright 2011 Tobias Rodaebel

This software is released under the Apache License, Version 2.0. You may obtain
a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Google App Engine is a trademark of Google Inc.


Requirements
------------

The Google App Engine SDK will be installed by zc.buildout. See the
buildout.cfg file.

Buildout needs Python and the tools contained in /bin and /usr/bin of a
standard installation of the Linux operating environment. You should ensure
that these directories are on your PATH and following programs can be found:

* Python 2.5.2+ (3.x is not supported!)


Building and Running the Application
------------------------------------

In order to set up a development environment for Silly Swarm, just follow these
steps.

Get the sources::

  $ git clone http://github.com/rodaebel/sillyswarm.git

Build the application::

  $ cd sillyswarm
  $ python bootstrap.py --distribute
  $ ./bin/buildout

Run the Web Socket service::

  $ python parts/google_appengine/tornado_websocket.py

Run the development appserver (from another shell)::

  $ ./bin/dev_appserver parts/sillyswarm

Then access the application using a web browser with the following URL::

  http://localhost:8080/


Uploading and Managing
----------------------

To upload application files, run::

  $ ./bin/appcfg update parts/sillyswarm

For a more detailed documentation follow this url::

  http://code.google.com/appengine/docs/python/tools/uploadinganapp.html
