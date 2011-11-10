from distutils.core import setup

setup(
    name='Partify',
    version='0.3',
    author='Fred Hatfull',
    author_email='fred.hatfull@gmail.com',
    packages=['partify'],
    scripts=['run.py'],
    url='http://www.partify.us',
    license='LICENSE.txt',
    description='Collaborative Spotify Music Streamer',
    long_description=open('README.rst').read(),
    install_requires=[
        "Flask >= 0.7.2",
        "Flask-WTF >= 0.5.2",
        "Flask-SQLAlchemy >= 0.15",
        "tornado >= 2.1.1"
    ],
)