"""
SatNOGS Client setup file
"""
from setuptools import find_packages, setup


setup(
    name='satnogsclient',
    version='1.0-pre',
    url='https://gitlab.com/librespacefoundation/satnogs/satnogs-client',
    author='SatNOGS project',
    author_email='dev@satnogs.org',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications :: Ham Radio',
    ],
    license='AGPLv3',
    description='SatNOGS Client',
    zip_safe=False,
    install_requires=[
        'APScheduler',
        'SQLAlchemy',
        'requests',
        'validators',
        'python-dateutil',
        'ephem',
        'pytz',
    ],
    entry_points={
        'console_scripts': ['satnogs-client=satnogsclient:main'],
    },
    include_package_data=True,
    packages=find_packages(),
)
