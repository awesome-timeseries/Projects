import argparse
from tsbench.adjust import adjust
from tsbench import runner 


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('algorithmName', help='name of algorithm to run')
    parser.add_argument('proportion', type=float, help='training dataset proportion')
    parser.add_argument('scoring', choices=['old', 'pei', 'new'], help='scoring mechanism(old, new, pei)')
    parser.add_argument('--delay', default=None, type=int, help='non-negative integer')
    
    args = parser.parse_args()
    assert 0.0 <= args.proportion < 1.0
    if not args.scoring=='old':
        assert args.delay >= 0

    adjust(args.algorithmName)
    print 'This might take a few minutes. Please wait...'
    import datetime
    starttime = datetime.datetime.now()
    runner.execute(args.algorithmName, args.proportion, args.scoring, args.delay)
    endtime = datetime.datetime.now()
    print (endtime - starttime).seconds, 's'
    
    print 'Successfully Done [Hooray]!'
