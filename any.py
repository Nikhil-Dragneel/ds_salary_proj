# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 16:07:10 2021

@author: Nikhil DragNeel
"""

import glassdoor_scraper as gs
import pandas as pd
path = "C:/Users/Nikhil DragNeel/gitTest/ds_salary_proj/chromedriver"
df = gs.get_jobs('data scientist',250,False,path,15)

df.to_csv('glassdoor_jobs.csv', index=False)

