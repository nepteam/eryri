nep
===

Nameless Education Platform

Prerequisite
------------

- RabbitMQ (AMQP)
- Redis (Cache, Session)
- MongoDB (Database)
- Python 2.7 (Python 3.3 is planned.)

Setup
-----

1. Check out the deployment script from `git@github.com:nepteam/automation.git`.
2. Install all initial dependencies with `make init_debian` or `make init_fedora`.
3. Run `puppet apply --verbose nep-core.pp`.

Start the service
-----------------

Just run `python server.py`