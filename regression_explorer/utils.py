###################################
# Some Util Functions
###################################

import pandas as pd
import numpy as np


def _range_cal(s,steps=5):
    range_step = (max(s) - min(s))//steps
    min_s = min(s)
    max_s = max(s)

    markers= {i : '{}'.format(round(min_s+steps*i)) for i in range(0,4)}

    return (min_s,max_s,markers)

def _format_coefs(model,x_feature,y_feature):
    coef_string = y_feature + " = "

    for coef in model.coef_:
        coef = round(coef,4)
        if coef >= 0:
            sign = ' +'
        else:
            sign = ' -'
        coef_string += sign + f'{abs(coef):.4f}*x'

    intercept = model.intercept_

    if intercept >= 0:
        sign = ' + '
    else:
        sign = ' - '

    coef_string += sign + f'{abs(round(intercept,2)):.3f}'

    return coef_string
