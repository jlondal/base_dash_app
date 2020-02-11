"""
A collection of functions to help manage data storage for users sessions
and callbacks across multiple workers.
"""

import pandas as pd
from pandas import HDFStore
import numpy as np
import datetime
import os



###################################
# Data Storage Utility Functions
###################################

# opens a dataframe linking it to a session id
def get_dataframe(session_id,app_name,path):
    df = pd.read_hdf(os.path.join(path,'%s.h5' % (session_id)), app_name)
    features = list(df.select_dtypes(include=[np.number]))
    dte_filter = list(df.select_dtypes(include=['datetime64']))[0]

    return (df, features, dte_filter)

# saves a dataframe linking it to a session id
def save_df(session_id,df,app_name,path):
    df.to_hdf(os.path.join(path,'%s.h5' % (session_id)), key=app_name)
