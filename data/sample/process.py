from __future__ import print_function
import sys
import pandas as pd
import numpy as np
from scipy.spatial import distance
from geopy.distance import vincenty
from collections import Counter

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def frange(x, y, jump):
    while x < y:
        yield x
        x += jump

def process(radius=1, subset=None):
    arrests = pd.read_csv('arrests.csv')
    arrests.dropna(inplace=True)
    cctv = pd.read_csv('cctv.csv')
    cctv.dropna(inplace=True)

    if subset is not None:
        arrests = arrests[1:subset]
        cctv = cctv[1:subset]

    all_arrests = len ( arrests )
    close = []
    far = list( arrests['IncidentOffense'].map( lambda x: x.lower() ) ) # far = all - close
    i=1
    for r in arrests.itertuples():
        a = r[15][1:-1].split(', ')
        a = ( float( a[0] ), float( a[1] ) )
        eprint("{} arrest out of {} for {}".format(i, all_arrests, radius))
        i += 1
        for rr in cctv.itertuples():
            c = rr[4][1:-1].split(', ')
            c = ( float( c[0] ), float( c[1] ) )
            dist = vincenty( a, c ).miles
            if dist < radius:
                close.append( r[8].lower() )
                far.remove( r[8].lower() )
                break

    print("{} arrests occured within {} mile(s) of a CCTV".format( len( close ), radius ) )
    close = Counter( close )
    for k, v in close.most_common():
        print(v,  "\t" +k)

    print("\n=================================================================\n")
    print("{} arrests did not occur within {} mile(s) of a CCTV".format( len( far ), radius ))
    far = Counter( far )
    for k, v in far.most_common():
        print(v, "\t" + k )

if __name__ == '__main__':
    for d in frange(0.1,1,0.1):
        process(d)
        print("=================================================================")
        print("=================================================================")
        print("=================================================================")
