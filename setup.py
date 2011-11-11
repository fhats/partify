import os
from distutils.core import setup

def gen_data_files(*dirs):
    """This function makes it easy to copy entire directory trees, which is useful for moving static assets needed by Partify (templates, JS, CSS, etc...).

    This code was graciously provided on StackOverflow by Scott Persinger at http://stackoverflow.com/questions/3596979/manifest-in-ignored-on-python-setup-py-install-no-data-files-installed ."""
    results = []

    for src_dir in dirs:
        for root,dirs,files in os.walk(src_dir):
            results.append((root, map(lambda f:root + "/" + f, files)))
    return results

setup(
    name='Partify',
    version='0.3',
    author='Fred Hatfull',
    author_email='fred.hatfull@gmail.com',
    packages=['partify', 'partify.forms'],
    data_files=gen_data_files("partify/static", "partify/templates", "partify/js", "bin"),
    scripts=['run_partify'],
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