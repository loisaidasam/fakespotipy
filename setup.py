
import os.path
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md')) as fp:
    long_description = fp.read()


setup(
    author="@LoisaidaSam",
    author_email="sam.sandberg@gmail.com",
    description="A fake spotipy client. For unit tests and stuff.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["spotify", "spotipy", "wrapper", "testing", "unit testing"],
    license="MIT",
    name="fakespotipy",
    packages=["fakespotipy"],
    test_suite="tests",
    url="https://github.com/rcrdclub/fakespotipy",
    version="0.7.0",
)
