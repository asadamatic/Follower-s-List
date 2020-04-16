
#This method is created by the following GitHub user
#https://gist.github.com/gajeshbhat

def convert_si_to_number(x):
    total_stars = 0
    if  'k' in x:
        if len(x) > 1:
            total_stars = float(x.replace('k', '')) * 1000 # convert k to a thousand
    elif 'm' in x:
        if len(x) > 1:
            total_stars = float(x.replace('m', '')) * 1000000 # convert M to a million
    elif 'b' in x:
        total_stars = float(x.replace('m', '')) * 1000000000 # convert B to a Billion
    elif ',' in x:

        total_stars = float(x.replace(',','')) # removing ,

    else:
        total_stars = int(x) # Less than 1000
    
    return int(total_stars)
