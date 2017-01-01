#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os.path as op


AUTHOR = 'Shadi Albarqouni'
SITENAME = 'Shadi Albarqouni'
SITEURL = 'https://albarqouni.github.io'
PATH = 'content'

SIDEBAR_NAME = 'Shadi Albarqouni'
SIDEBAR_SUBNAME = 'Deep Learning | Medical Informatics | Entrepreneurship'
SIDEBAR_EMAIL = '<i>firstname</i>.<i>lastname</i>@tum.de'
SIDEBAR_LOCATION = 'Munich, Germany'
SIDEBAR_TAGS = ['medical',
                'python',
                'ml',
                'maths',
                ]

DEFAULT_DATE = 'fs'
WITH_FUTURE_DATES = True
FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)'
STATIC_PATHS = ['images', 'pdfs', 'widgets']
PAGE_EXCLUDES = ['widgets', '.ipynb_checkpoints']
ARTICLE_EXCLUDES = ['widgets', '.ipynb_checkpoints']
EXTRA_PATH_METADATA = {
    'images/favicon.png': {'path': 'favicon.png'},
}

#THEME = './pelican-themes/blue-penguin'
THEME = './themes/pure'

MD_EXTENSIONS = ['codehilite(css_class=highlight,'
                 'guess_lang=False,linenums=False)',
                 'headerid',
                 'extra']
DEFAULT_PAGINATION = 5
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)
PLUGIN_PATHS = ['pelican-plugins', 'plugins']
PLUGINS = ['render_math',
           'summary',
           'neighbors',
	   'ipynb.markup'
           ]

MARKUP = ('md', 'ipynb')
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False
DIRECT_TEMPLATES = ('index', 'archives')
ARCHIVES_SAVE_AS = 'archives/index.html'
ARTICLE_URL = '{slug}/'
ARTICLE_SAVE_AS = '{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'
TAGS_SAVE_AS = ''
AUTHOR_URL = ''
AUTHOR_SAVE_AS = ''
CATEGORY_URL = ''
CATEGORY_SAVE_AS = ''
TWITTER_USERNAME = 'ShadiAlbarqouni'
GITHUB_USERNAME = 'albarqouni'
LINKEDIN_USERNAME = 'shadialbarqouni'
STATCOUNTER = ''
DISQUS_SITENAME = 'shadialbarqouni'
MENUITEMS = [('Home', '/'),
             ('Projects', '/projects/'),
             ('Books', '/books/'),
             ('About', '/about/'),
             ]
DATE_FORMATS = {
    'en': '%Y-%m-%d',
}

TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('CAMP@TUM', 'http://campar.in.tum.de/Main/ShadiAlbarqouni'),
         ('LinkedIn', 'https://de.linkedin.com/in/shadialbarqouni'),
         ('ResearchGate', 'https://www.researchgate.net/profile/Shadi_Albarqouni'),)

# Social widget
SOCIAL = (
    ('github', 'https://github.com/albarqouni/'),
    ('twitter-square', 'https://twitter.com/ShadiAlbarqouni'),)

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True


# pure theme
COVER_IMG_URL = 'images/shadi_cover.jpg'
PROFILE_IMAGE_URL = 'images/favicon.png'
DISQUS_SITENAME = 'shadialbarqouni'
TAGLINE = 'Deep Learning | Medical Informatics | Entrepreneurship'
