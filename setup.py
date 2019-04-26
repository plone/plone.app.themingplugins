from setuptools import find_packages
from setuptools import setup


version = '1.1'

setup(
    name='plone.app.themingplugins',
    version=version,
    description="Plugins providing advanced plone.app.theming integration",
    long_description=open("README.rst").read()
    + "\n"
    + open("CHANGES.rst").read(),
    classifiers=["Framework :: Plone", "Programming Language :: Python"],
    keywords='plone.app.theming diazo jbot views',
    author='Martin Aspeli',
    author_email='optilude@gmail.com',
    url='http://pypi.python.org/pypi/plone.app.theming.plugins',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
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
