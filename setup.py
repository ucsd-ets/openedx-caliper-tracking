import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='CaliperTracking',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='Caliper Tracking app can be used to transform edx traditional events into caliper standard events.',
    long_description=README,
    url='https://github.com/danialmalik/openedx-caliper_tracking.git',
    author='Danial Malik',
    author_email='danialmalik321@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
