from setuptools import setup

# add to pypi with the following commands:
'''
python setup.py register -r pypi
python setup.py sdist upload -r pypi
pip install honeywell_thermostat --upgrade
'''

setup(
    name='honeywell_thermostat',
    packages=['honeywell_thermostat'],
    version='1.1.13',
    description='Python API for Honeywell thermostats',
    author='Jordan Thompson',
    author_email='Jordan@ThompCo.com',
    download_url='https://github.com/jorythompson/thermostat',
    url='https://github.com/jorythompson/thermostat',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='develoment tools',
    install_requires=[],

)