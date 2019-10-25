*************************
Open edX Caliper Tracking
*************************


Description
###########

Open edX Caliper Tracking can be used to transform the edX traditional event logs into `Caliper Analytics Specifications <https://www.imsglobal.org/activity/caliper>`_ provided by `IMS Global <http://imsglobal.org>`_. Generated logs can be consumed by any analytics application which is compatible with Caliper Standard.

Installation
############

To install **openedx-caliper-tracking** in your Open edX installation, please add the following line to your requirements file. (For most Open edX installations it should be located at edx-platform/requirements/edx/base.txt)::

    openedx-caliper-tracking==0.11.3

Usage
#####

To enable and use `openedx-caliper-tracking`:

1. Add ``ENABLE_EVENT_CALIPERIZATION`` flag under ``FEATURES`` in the following files:

 * ``/edx/app/edxapp/lms.env.json``
 * ``/edx/app/edxapp/cms.env.json``

These files should be located at ``/edx/app/edxapp/`` directory, see the example below::

    "FEATURES": {
        ...

        "ENABLE_EVENT_CALIPERIZATION": true,

        ...
    }

2. Add the following lines::

    if FEATURES.get('ENABLE_EVENT_CALIPERIZATION'):
        INSTALLED_APPS.insert(
            INSTALLED_APPS.index('eventtracking.django.apps.EventTrackingConfig'),
            'openedx_caliper_tracking'
        )

in the following files:

- ``lms/envs/aws.py (production.py for ironwood release)``

- ``cms/envs/aws.py (production.py for ironwood release)``


Location of Transformed Logs
****************************

Transformed events are logged using **'logging.handlers.SysLogHandler'** with **'facility: local2'**.

We need to create output files manually and set appropriate permissions for syslog user. To do so, please follow the steps below:

1. Create a log file with read/write permissions given to **syslog** user e.g: **/edx/var/log/caliper-analytics/caliper.log**

2. Create a mapping for **'local2'** in the configuration files present in **/etc/rsyslog.d/** ::

    local2.*                 /edx/var/log/caliper-analytics/caliper.log


Sending logs to external API
############################

Using the app, we can also send the transformed event logs to some third party broker API (e.g. kafka). To do this, we have to add the following configurations

**Note**: Set these settings only if you want to send the logs to some external consumer.

1. Add ``ENABLE_CALIPER_EVENTS_DELIVERY`` flag under ``FEATURES`` in the following files:

 * ``/edx/app/edxapp/lms.env.json``
 * ``/edx/app/edxapp/cms.env.json``

These files should be located at ``/edx/app/edxapp/`` directory, see the example below::

    "FEATURES": {
        ...

        "ENABLE_CALIPER_EVENTS_DELIVERY": true,

        ...
    }

2. Add the key ``CALIPER_DELIVERY_ENDPOINT`` and its value in the ``lms.env.json`` and ``cms.env.json`` files.
3. Add the key ``CALIPER_DELIVERY_AUTH_TOKEN`` and its value in the ``lms.auth.json`` and ``cms.auth.json`` files.
4. Add the following lines::

    CALIPER_DELIVERY_ENDPOINT = ENV_TOKENS.get('CALIPER_DELIVERY_ENDPOINT')
    CALIPER_DELIVERY_AUTH_TOKEN = AUTH_TOKENS.get('CALIPER_DELIVERY_AUTH_TOKEN')


in the following files:

- ``lms/envs/aws.py (production.py for ironwood release)``

- ``cms/envs/aws.py (production.py for ironwood release)``


License
#######

The code in this repository is licensed under the GPL v3.0 unless otherwise noted. Please see `LICENSE <./LICENSE>`_ for details.


How To Contribute
#################

To contribute, please make a pull request in this repositry on Github: `Open edX Caliper Tracking <https://github.com/ucsd-ets/openedx-caliper-tracking>`_. If you have any question or issue, please feel free to open an issue on Github: `Open edX Caliper Tracking <https://github.com/ucsd-ets/openedx-caliper-tracking>`_.


Contributors
############

* `Muhammad Zeeshan <https://github.com/zee-pk>`_
* `Tasawer Nawaz <https://github.com/tasawernawaz>`_
* `Saad Ali <https://github.com/NIXKnight>`_
* `Husnain Raza Ghaffar <https://github.com/HusnainRazaGhaffar>`_
* `Aroosha Arif <https://github.com/arooshaarif>`_
* `Osama Arshad <https://github.com/asamolion>`_
* `Tehreem Sadat <https://github.com/tehreem-sadat>`_
* `Muhammad Arslan <https://github.com/arslanhashmi>`_
* `Danial Malik <https://github.com/danialmalik>`_
* `Hamza Farooq <https://github.com/HamzaIbnFarooq>`_
* `Hassan Tariq <https://github.com/imhassantariq>`_
* `Muhammad Umar Khan <https://github.com/mumarkhan999>`_
