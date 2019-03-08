*************************
Open edX Caliper Tracking
*************************


Description
###########

Open edX Caliper Tracking can be used to transform the edx traditional event logs into `IMS Caliper Standard <http://imsglobal.org/sites/default/files/caliper/v1p1/caliper-spec-v1p1/caliper-spec-v1p1.html>`_ format. Then those logs can be used with any analytics application that is compatible with Caliper Standard events.

Installation
############

To install **openedx-caliper-tracking** in your Open edX installation, please add the following line to your requirements file. (For most Open edX installations it is located at edx-platform/requirements/edx/base.txt)::

    openedx-caliper-tracking==0.9.0


Usage
#####

To enable and use `openedx-caliper-tracking`:

Set the value of ``ENABLE_EVENT_CALIPERIZATION`` flag under ``FEATURES`` in the following files:

 * ``/edx/app/edxapp/lms.env.json``
 * ``/edx/app/edxapp/cms.env.json``

these files should be located at ``/edx/app/edxapp/`` directory::


    "FEATURES": {
        ...

        "ENABLE_EVENT_CALIPERIZATION": true,

    }


Location of Transformed Logs
****************************

Transformed event logs can be found in ``/edx/var/logs/tracking/tracking.log`` file.


License
#######

The code in this repository is licensed under the GPL 3.0 unless otherwise noted.

Please see `LICENSE <./LICENSE>`_ for details.


How To Contribute
#################

To contribute, please make the PR in this repositry on Github: `Open edX Caliper Tracking <https://github.com/ucsd-ets/openedx-caliper-tracking>`_

If you have any issues or questions, please feel free to open an issue on Github: `Open edX Caliper Tracking <https://github.com/ucsd-ets/openedx-caliper-tracking>`_


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
