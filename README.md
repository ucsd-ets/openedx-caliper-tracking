to make dist:

```
python setup.py sdist
```

and to install app:

```
pip install -e <path/to/app-root-dir>
```

To run the app properly, "caliper_tracking" should be mentioned in "INSTALLED_APPS" before "eventtracking" and after "third_party_auth".

