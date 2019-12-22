# -*- coding: utf-8 -*-
import talib

def handler(event, context):
  return talib.get_functions()[:5] 