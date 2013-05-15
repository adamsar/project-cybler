import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = ['httplib2', 'feedparser', 'lxml', 'BeautifulSoup4', 'numpy', 'scipy', 'nltk', 'scikit-learn']

setup(name='cybler_tasks',
      version='0.0',
      description='cybler tasks for data ingestion',
      author="AABG Productions",
      author_email='adamsar@gmail.com',
      url='',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="tests"
      )

