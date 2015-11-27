import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='mezzanine-developer-extension',
    version='0.2.2',
    packages=['mezzanine_developer_extension'],
    include_package_data=True,
    license='BSD License',
    description='Removes the wysiwyg editor and provides a few handful shortcuts to generate terminal-looking divisions, tip bubbles and log divisions',
    long_description=README,
    url='https://github.com/educalleja/mezzanine-developer-extension',
    author='Eduardo Calleja',
    author_email='e.calleja.garcia@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
