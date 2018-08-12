__version__ = '0.0.1'

NAME = 'hacktrack'
MAINTAINER = 'Ross Markello and friends'
EMAIL = 'rossmarkello@gmail.com'
VERSION = __version__
# BIDS/watchtower doesn't have a license file...
LICENSE = 'Copyright reserved by Berkeley Institute for Data Science'
DESCRIPTION = ('A toolbox for hackathons')
LONG_DESCRIPTION = ('')
URL = 'http://github.com/rmarkello/{name}'.format(name=NAME)
DOWNLOAD_URL = ('https://github.com/rmarkello/{name}/archive/{ver}.tar.gz'
                .format(name=NAME, ver=__version__))

INSTALL_REQUIRES = [
    'matplotlib',
    'numpy',
    'pandas',
    'seaborn',
    'tqdm'
]

TESTS_REQUIRE = [
]

PACKAGE_DATA = {
    'hacktrack': ['data/*', 'data/*/*']
}
