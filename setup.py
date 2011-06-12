from setuptools import setup, find_packages

version = '1.0b1'

setup(name='plone.app.themingplugins',
      version=version,
      description="Plugins providing advanced plone.app.theming integration",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
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
          'setuptools',
          'plone.app.theming',
          'zope.interface',
          'zope.dottedname',
          'plone.resource',
          'zope.configuration',
          'z3c.jbot',
      ],
      extras_require = {
          'test': ['plone.app.testing']
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
