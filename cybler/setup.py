import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()

requires = ['pyramid', 'WebError', 'pymongo', 'httplib2', 'feedparser']

setup(name='cybler',
      version='0.0',
      description='cybler',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author="AABG Productions",
      author_email='adamsar@gmail.com',
      url='',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="tests",
      entry_points = """\
      [paste.app_factory]
      main = cybler:main
      """,
      paster_plugins=['pyramid'],
      )

