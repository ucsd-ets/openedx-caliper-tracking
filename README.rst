*************************
Open edX Caliper Tracking
*************************


Description
###########

Open edX Caliper Tracking can be used to transform the edX traditional event logs into `Caliper Analytics Specifications <https://www.imsglobal.org/activity/caliper>`_ provided by `IMS Global <http://imsglobal.org>`_. Generated logs can be consumed by any analytics application which is compatible with Caliper Standard.

Installation
############

To install **openedx-caliper-tracking** in your Open edX installation, please add the following line to your requirements file. (For most Open edX installations it should be located at edx-platform/requirements/edx/base.txt)::

    openedx-caliper-tracking==0.10.2

Usage
#####

To enable and use `openedx-caliper-tracking`:

Please add ``ENABLE_EVENT_CALIPERIZATION`` flag under ``FEATURES`` in the following files:

 * ``/edx/app/edxapp/lms.env.json``
 * ``/edx/app/edxapp/cms.env.json``

These files should be located at ``/edx/app/edxapp/`` directory, see the example below::

    "FEATURES": {
        ...

        "ENABLE_EVENT_CALIPERIZATION": true,

    }


Location of Transformed Logs
****************************

Transformed events are logged using **'logging.handlers.SysLogHandler'** with **'facility: local2'**.

We need to create output files manually and set appropriate permissions for syslog user. To do so, please follow the steps below:

1. Create a log file with read/write permissions given to **syslog** user e.g: **/edx/var/log/caliper-analytics/caliper.log**

2. Create a mapping for **'local2'** in the configuration files present in **/etc/rsyslog.d/** ::

    local2.*                 /edx/var/log/caliper-analytics/caliper.log


License
#######

The code in this repository is licensed under the GPL v3.0 unless otherwise noted. Please see `LICENSE <./LICENSE>`_ for details.


How To Contribute
#################

To contribute, please make a pull request in this repositry on Github: `Open edX Caliper Tracking <https://github.com/ucsd-ets/openedx-caliper-tracking>`_. If you have any question or issue, please feel free to open an issue on Github: `Open edX Caliper Tracking <https://github.com/ucsd-ets/openedx-caliper-tracking>`_.


Contributors
############

* `Muhammad Zeeshan <https://github.com/zee-pk>`_
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