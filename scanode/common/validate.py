# Verification functions


def verify(exp, err_msg):
    '''Check 'exp' to be True and raises an exception if it is False.'''

    if not exp:
        raise Exception(err_msg)
