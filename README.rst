*************************
Open edX Caliper Tracking
*************************

Open edX Caliper Tracking can be used to transform the edX traditional event logs into `Caliper Analytics Specifications <https://www.imsglobal.org/activity/caliper>`_ provided by `IMS Global <http://imsglobal.org>`_. Generated logs can be consumed by any analytics application which is compatible with Caliper Standard. All the transformed logs are `Caliper Certified <https://site.imsglobal.org/certifications/university-of-california-san-diego/144956/openedx-caliper-tracking#cert_pane_nid_169481>`_.


Installation
############

To install **openedx-caliper-tracking** in your Open edX instance, please add the following line to your ``requirements file``. (For most Open edX installations it should be located at ``edx-platform/requirements/edx/base.txt``).
::

    openedx-caliper-tracking==0.11.8

For manual installation:
::

    pip install openedx-caliper-tracking

Configuration
#############

To enable and use `openedx-caliper-tracking`:

1. Add ``ENABLE_EVENT_CALIPERIZATION`` flag under ``FEATURES`` in the following files:

- ``lms.env.json``
- ``cms.env.json``

These files should be located at ``/edx/app/edxapp/`` directory, see the example below:
::

    "FEATURES": {
        ...

        "ENABLE_EVENT_CALIPERIZATION": true,

        ...
    }

2. Add the following lines of code:
::

    if FEATURES.get('ENABLE_EVENT_CALIPERIZATION'):
        INSTALLED_APPS.insert(
            INSTALLED_APPS.index('eventtracking.django.apps.EventTrackingConfig'),
            'openedx_caliper_tracking'
        )

in the following files:

- ``lms/envs/aws.py (production.py for ironwood release)``

- ``cms/envs/aws.py (production.py for ironwood release)``

**Note:**

    Must make sure that after doing all the required changes in ``env`` (``lms.env.json`` and ``cms.env.json``) and ``auth`` (``lms.auth.json`` and ``cms.auth.json``) files you restart the server to reflect the changes that you have made.

Sending logs to external APIs (Optional)
########################################

There are two ways we can send caliper transformed logs to any external API

- Rest API
- Kafka

Using REST API
**************

To do this, we have to add the following configurations

1. Add ``ENABLE_CALIPER_EVENTS_DELIVERY`` flag under ``FEATURES`` in the following files:

- ``lms.env.json``

- ``cms.env.json``

These files should be located at ``/edx/app/edxapp/`` directory, see the example below:
::

    "FEATURES": {
        ...

        "ENABLE_CALIPER_EVENTS_DELIVERY": true,

        ...
    }

2. Add the key ``CALIPER_DELIVERY_ENDPOINT`` and its value in the  ``env`` files (``lms.env.json`` and ``cms.env.json``).
3. Add the key ``CALIPER_DELIVERY_AUTH_TOKEN`` and its value in the ``auth`` files ( ``lms.auth.json`` and ``cms.auth.json``).
4. Add the following lines of code:

::

    if FEATURES.get('ENABLE_CALIPER_EVENTS_DELIVERY'):
        CALIPER_DELIVERY_ENDPOINT = ENV_TOKENS.get('CALIPER_DELIVERY_ENDPOINT')
        CALIPER_DELIVERY_AUTH_TOKEN = AUTH_TOKENS.get('CALIPER_DELIVERY_AUTH_TOKEN')

in the following files:

- ``lms/envs/aws.py (production.py for ironwood release)``

- ``cms/envs/aws.py (production.py for ironwood release)``

Using Kafka Broker API
**********************

To do this, we have to add the following configurations

1. Add ``ENABLE_KAFKA_FOR_CALIPER`` flag under ``FEATURES`` in the following files:

- ``lms.env.json``

- ``cms.env.json``

These files should be located at ``/edx/app/edxapp/`` directory, see the example below:
::

    "FEATURES": {
        ...

        "ENABLE_KAFKA_FOR_CALIPER": true,

        ...
    }

2. Add the following keys and their values in the ``lms.env.json`` and ``cms.env.json`` files.
::

    "CALIPER_KAFKA_SETTINGS": {
        "MAXIMUM_RETRIES": <integer>,
        "END_POINT": "kafka endpoint",
        "TOPIC_NAME": "topic name",
        "ERROR_REPORT_EMAIL": "support@example.com"
    }

+------------------+------------------------------------------------------------------------------+
|Keys              |                                  Description                                 |
+==================+==============================================================================+
|MAXIMUM_RETRIES   |Number of times the app will try to send the logs to Kafka in case of failure |
+------------------+------------------------------------------------------------------------------+
|END_POINT         |URL for Kafka Broker                                                          |
+------------------+------------------------------------------------------------------------------+
|TOPIC_NAME        |Topic name for the Kafka broker                                               |
+------------------+------------------------------------------------------------------------------+
|ERROR_REPORT_EMAIL|Email Address to notify when number of failures exceeds the MAXIMUM_RETRIES   |
+------------------+------------------------------------------------------------------------------+

3. Add the following lines of code:
::

    if FEATURES.get('ENABLE_KAFKA_FOR_CALIPER'):
        CALIPER_KAFKA_SETTINGS = ENV_TOKENS.get('CALIPER_KAFKA_SETTINGS')

in the following files:

- ``lms/envs/aws.py (production.py for ironwood release)``

- ``cms/envs/aws.py (production.py for ironwood release)``

Location of Transformed Logs
############################

**Note:** This doesn't work locally.

Transformed events are logged using ``'logging.handlers.SysLogHandler'`` with ``'facility: local2'``.

We need to create output files manually and set appropriate permissions for syslog user. To do so, please follow the steps below:

1. Create a log file with read/write permissions given to ``syslog`` user (e.g: ``/edx/var/log/caliper-analytics/caliper.log``).
::

    cd /edx/var/log
    mkdir -p caliper-analytics && cd caliper-analytics
    touch caliper.log
    chown syslog caliper.log

2. Create a mapping for ``'local2'`` in the configuration files present in ``/etc/rsyslog.d/``  (e.g: in ``99-edx.conf``).

::

    local2.*                 /edx/var/log/caliper-analytics/caliper.log;tracking

3. Run the following command on server to restart the rsyslog daemon:

::

    sudo service rsyslog restart

Location of Logs Whose Delivery to Kafka is failed
##################################################


**Note:**

    This doesn't work locally. Do this only if you are sending logs to external source using Kafka broker API.

Transformed events are logged using ``'logging.handlers.SysLogHandler'`` with ``'facility: local3'``.

We need to create output files manually and set appropriate permissions for syslog user. To do so, please follow the steps below:

1. Create a log file with read/write permissions given to ``syslog`` user (e.g: ``/edx/var/log/caliper-analytics/delivery_failure.log``).
::

    cd /edx/var/log
    mkdir -p caliper-analytics && cd caliper-analytics
    touch delivery_failure.log
    chown syslog delivery_failure.log

2. Create a mapping for ``'local3'`` in the configuration files present in ``/etc/rsyslog.d/``  (e.g: in ``99-edx.conf``).

::

    local3.*                 /edx/var/log/caliper-analytics/delivery_failure.log;tracking

3. Run the following command on server to restart the rsyslog daemon:

::

    sudo service rsyslog restart

Running Tests Locally
#####################

To run the unit tests of this app locally, follow the following steps:

- Clone the repository

::

    git clone git@github.com:ucsd-ets/openedx-caliper-tracking.git

- Run the following command in the same directory in which you have cloned the repository

::

    sudo ./openedx-caliper-tracking/openedx_caliper_tracking/tests/local_test_script.sh

License
#######

The code in this repository is licensed under the GPL v3.0 unless otherwise noted. Please see `LICENSE <./LICENSE>`_ for details.


How To Contribute
#################

To contribute, please make a pull request in the `repository <https://github.com/ucsd-ets/openedx-caliper-tracking>`_ on Github . If you have any questions or issues, please feel free to open an issue on Github: `Open edX Caliper Tracking <https://github.com/ucsd-ets/openedx-caliper-tracking/issues/new>`_.


Contributors
############

* `Muhammad Zeeshan <https://github.com/zee-pk>`_
* `Tasawer Nawaz <https://github.com/tasawernawaz>`_
* `Aroosha Arif <https://github.com/arooshaarif>`_
* `Osama Arshad <https://github.com/asamolion>`_
* `Danial Malik <https://github.com/danialmalik>`_
* `Hamza Farooq <https://github.com/HamzaIbnFarooq>`_
* `Hassan Tariq <https://github.com/imhassantariq>`_
* `Muhammad Umar Khan <https://github.com/mumarkhan999>`_
* `Tehreem Sadat <https://github.com/tehreem-sadat>`_
* `Muhammad Arslan <https://github.com/arslanhashmi>`_
* `Saad Ali <https://github.com/NIXKnight>`_
* `Husnain Raza Ghaffar <https://github.com/HusnainRazaGhaffar>`_
