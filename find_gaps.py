"""find_gaps.py finds missing files in a sequence based on date

Usage: find_gaps.py --chars=<start,end> [--fmt=<fmt>] [--start=<YYYY-mm-dd_HHMM>] [--end=<YYYY-mm-dd_HHMM>]  [--freq=<str>] [--date-only] [--verbose]  [--help] <files>...

    Options:
        --chars=<start,end> start and end index of the date part within filenames
        --fmt=<fmt>         date format within filenames [default: "%Y-%m-%d_%H"]
        --start=<start>     optional start date of file sequence, if not specified, first file is use
        --end=<end>         optional end date of file sequence, if not specified, last file is used
        --freq=<hours>      number of hours between file times, if None, difference between first two files is used
        --date-only         print missing dates, not full filename
        --verbose           print more information
        --help              print help information
        <files>             files to check for gaps"""

import docopt
import os
import sys
import time,datetime
from dateutil import rrule

def parsedate(token, fmt):
    ttuple = time.strptime(token, fmt)[0:6]
    return datetime.datetime(*ttuple)

        
def main(args):
    files = map(os.path.basename, args['<files>'])
    chars = map(int, args['--chars'].split(','))
    assert len(chars)==2
    
   
    
    # start index, end index
    si = chars[0]
    ei = chars[1]
    
    # supply format argument to parser function
    fmt = args['--fmt']
    parse = lambda s: parsedate(s, fmt)

    dateparts = [f[si:ei] for f in files]
    # get the remaining, non-date characters to reconstruct filenames
    # assume this is fixed between files
    f0 = files[0]
    namestart = f0[0:si]
    nameend = f0[ei:]

    if args['--verbose']:
        print dateparts[0]
    filedates = [parse(d) for d in dateparts]
   
   
    if args.get('--start'):
        start=parse(args['--start'])
    else:
        start = filedates[0]

    if args.get('--end'):
        end=parse(args['--end'])
    else:
        end = filedates[-1]


    if args.get('--freq'):
        freq  = int(args['--freq'])
    else:
        delta = filedates[1] - filedates[0]
        freq = delta.days*24+delta.seconds/(60*60)
    

    rule = rrule.rrule(dtstart=start, until=end, freq=rrule.HOURLY, interval=freq)
    alldates = list(rule)

    missing = [d for d in alldates if d not in filedates]


    for d in missing:
        if args['--date-only']:
            print d.strftime(fmt)
        else:
            print '%s%s%s' %(namestart,d.strftime(fmt),nameend)

    if args['--verbose']:
        print '********************************'
        print ' sequence start: %s' % start
        print ' sequence end: %s'   % end
        print ' %d files expected'  % len(alldates)
        print ' %d files missing'   % len(missing)
        print '********************************'

if __name__ == '__main__':
    args = docopt.docopt(__doc__, sys.argv[1:])
    main(args)

