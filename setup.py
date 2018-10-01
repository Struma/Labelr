from setuptools import setup

setup(name='labelr',
      version='2.0',
      description='label images for sci systematics',
      url='http://github.com/Struma/Labelr',
      author='Struma',
      author_email='struma_dev@protonmail.com',
      license='GNUv3',
      packages=['labelr'],
      install_requires=[
          'Pillow',
          'py3exiv2'
      ],
      scripts=['bin/labelr'],
      include_package_data=True,
      zip_safe=False)
