from setuptools import setup, find_packages

setup(
    name='Braintree-Transaction-Statistics-GUI',
    version='2.0.0',
    packages=find_packages(),
    url='',
    license='',
    author='Rickey Serna',
    author_email='rickeyserna7@live.com',
    description='A Python project which creates a GUI displaying statistics on transactions in a Braintree gateway.',
    entry_points={
        'console_scripts': [
            'runstats=BT_stats_GUI.main:main',
        ],
    },
)