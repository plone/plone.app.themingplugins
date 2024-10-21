from setuptools import find_packages
from setuptools import setup


version = '1.3.dev0'

setup(
    name='plone.app.themingplugins',
    version=version,
    description="Plugins providing advanced plone.app.theming integration",
    long_description=open("README.rst").read()
    + "\n"
    + open("CHANGES.rst").read(),
    classifiers=[
       "Framework :: Plone",
       "License :: OSI Approved :: GNU General Public License (GPL)",
	   "Development Status :: 5 - Production/Stable",
       "Programming Language :: Python",
	   "Programming Language :: Python :: 2",
	   "Programming Language :: Python :: 2.7",
	   "Programming Language :: Python :: 3",
	   "Programming Language :: Python :: 3.7",
	   "Programming Language :: Python :: 3.8",
	   "Programming Language :: Python :: 3.9",
	   "Programming Language :: Python :: 3.10",
	   "Programming Language :: Python :: 3.11",
	   "Programming Language :: Python :: 3.12"],
    keywords='plone.app.theming diazo jbot views',
    author='Martin Aspeli',
    author_email='optilude@gmail.com',
    url='http://pypi.python.org/pypi/plone.app.theming.plugins',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=2.7,!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, <3.13",
    install_requires=[
        'plone.app.theming',
        'plone.resource',
        'setuptools',
        'six',
        'z3c.jbot',
        'zope.configuration',
        'zope.dottedname',
        'zope.interface',
    ],
    extras_require={'test': ['plone.app.testing']},
    entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
