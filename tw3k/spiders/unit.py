import scrapy, os

import pandas as pd

from urllib.parse import parse_qsl
from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.selector import Selector