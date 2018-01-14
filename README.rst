=======================
Zwift Mobile API client
=======================


.. image:: https://img.shields.io/pypi/v/zwift-client.svg
        :target: https://pypi.python.org/pypi/zwift-client

.. image:: https://img.shields.io/travis/jsmits/zwift-client.svg
        :target: https://travis-ci.org/jsmits/zwift-client

.. image:: https://pyup.io/repos/github/jsmits/zwift-client/shield.svg
     :target: https://pyup.io/repos/github/jsmits/zwift-client/
     :alt: Updates


Python port of the Zwift Mobile API Javascript client: zwift-mobile-api_.

* Free software: MIT license


Installation
------------

::

    $ pip install zwift-client


Usage
-----


Client
++++++

::

    >>> from zwift import Client
    >>> username = 'your-username'
    >>> password = 'your-password'
    >>> player_id = your-player-id
    >>> client = Client(username, password)


Profile
+++++++

::

    >>> profile = client.get_profile()
    >>> profile.profile  # fetch your profile data
    >>> profile.followers
    >>> profile.followees
    >>> profile.get_activities()  # metadata of your activities
    >>> profile.latest_activity  # metadata of your latest activity


Activity
++++++++

::

    >>> activity = client.get_activity(player_id)
    >>> activities = activity.list()  # your activities
    >>> latest_activity_id = activities[0]['id']
    >>> activity.get_activity(latest_activity_id)  # metadata of your latest activity
    >>> activity.get_data(latest_activity_id)  # processed FIT file data


World
+++++

::

    >>> world = client.get_world(1)  # get world with id 1
    >>> world.players  # players currently present in this world
    >>> world.player_status(player_id) # current player status information like speed, cadence, power, etc.


Credits
---------

This package was created with cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _zwift-mobile-api: https://github.com/Ogadai/zwift-mobile-api

