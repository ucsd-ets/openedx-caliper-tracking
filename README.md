# Caliper Tracking

## Description

Caliper Tracking can be used to transform the edx tradition events into [IMS Caliper Standard](http://imsglobal.org/sites/default/files/caliper/v1p1/caliper-spec-v1p1/caliper-spec-v1p1.html) format. Then those events can be used with any analytics application that is compatible with Caliper Standard events.

## Installation

To install **`caliper-tracking`** run the following command inside your virtual environment:

```sh
pip install git+https://github.com/ucsd-ets/caliper-tracking.git@master#egg=caliper-tracking
```

The dependency can also be added to the requirements files of Open edX platform.

## Usage

To enable and use `caliper-tracking`

Add/Enable the `ENABLE_EVENT_CALIPERIZATION` flag in `FEATURES` in the following files:
 * `/edx/app/edxapp/lms.env.json`
 * `/edx/app/edxapp/cms.env.json`

which are located at `/edx/app/edxapp/` directory.

```
"FEATURES": {
    ...
    "ENABLE_EVENT_CALIPERIZATION": true,
}
```

Restart your server.
Transformed event logs can be found in `/edx/var/logs/tracking/tracking.log`.
