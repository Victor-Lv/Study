#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
logging.basicConfig(filename='logger.log', level=logging.INFO)


s = '0'
n = int(s)
logging.info('n = %d' , n)
logging.debug('n = %d' , n)
logging.error('n = %d' , n)
logging.warning('n = %d' , n)
print(10 / n)
