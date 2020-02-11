import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='openedx-caliper-tracking',
    version='0.11.8',
    packages=find_packages(),
    include_package_data=True,
    license='GPL 3.0',
    description='Open edX Caliper Tracking app can be used to transform Open edX tracking events into Caliper standard compliant events.',
    long_description=README,
    url='https://github.com/ucsd-ets/caliper-tracking',
    author='UC San Diego',
    install_requires=[
        'kafka-python==1.4.7'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
