# -*- coding: utf-8 -*-
"""
Fill in your API info here, and rename to spotifyConstants.py
"""

import os
from dotenv import load_dotenv

#loading environment variables from .env file 
load_dotenv()

#loading spotify account variables
myUser = os.getenv("myUser")
myClientID = os.getenv("myClientID")
myClientSecret = os.getenv("myClientSecret")
myRedirect = os.getenv("myRedirect")