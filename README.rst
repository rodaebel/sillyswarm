===========
Silly Swarm
===========

Browser game to demonstrate TyphoonAE's Web Socket handler.


Copyright and License
---------------------

Copyright 2011 Tobias Rodaebel

This software is released under the Apache License, Version 2.0. You may obtain
a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0


Online Demo
-----------

In order to play Silly Swarm, access the following URL with a HTML5 Web Socket
capable browser like Google Chrome or Safari:

  http://sillyswarm.appspot.com


Requirements
------------

The GAE SDK will be installed by zc.buildout. See the buildout.cfg file.

Buildout needs Python and the tools contained in /bin and /usr/bin of a
standard installation of the Linux operating environment. You should ensure
that these directories are on your PATH and following programs can be found:

* Python 2.5.2+ (3.x is not supported!)
* virtualenv (optional)


Building and Running the Application
------------------------------------

We recommend to install this buildout into a virtualenv in order to obtain
isolation from any 'system' packages you've got installed in your Python
version.

Install virtualenv::

  $ virtualenv --distribute sillyswarm-env
  $ cd sillyswarm-env
  $ git clone http://github.com/rodaebel/sillyswarm.git

Build the application::

  $ cd sillyswarm
  $ ../bin/python bootstrap.py --distribute
  $ ./bin/buildout

Run the Web Socket service::

  $ python parts/google_appengine/tornado_websocket.py

Run the development appserver::

  $ ./bin/dev_appserver parts/sillyswarm

Then access the application using a web browser with the following URL::

  http://localhost:8080/


Uploading and Managing
----------------------

To upload application files, run::

  $ ./bin/appcfg update parts/sillyswarm

For a more detailed documentation follow this url::

  http://code.google.com/appengine/docs/python/tools/uploadinganapp.html
