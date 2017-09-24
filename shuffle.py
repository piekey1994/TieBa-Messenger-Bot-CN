import os
import sys
import random

import tempfile
from subprocess import call

'''
This code comes from shuffle.py of
nematus proejct (https://github.com/rsennrich/nematus)
'''

def main(files, temporary=False):

    tf_os, tpath = tempfile.mkstemp()
    tf = open(tpath, 'w',encoding='utf8')

    fds = [open(ff,encoding='utf8') for ff in files]

    for l in fds[0]:
        lines = [l.strip()] + [ff.readline().strip() for ff in fds[1:]]
        tf.write("|||".join(lines)+'\n')
        #print ("|||".join(lines),file=tf)

    [ff.close() for ff in fds]
    tf.close()

    lines = open(tpath, 'r',encoding='utf8').readlines()
    random.shuffle(lines)

    if temporary:
        fds = []
        for ff in files:
            path, filename = os.path.split(os.path.realpath(ff))
            fds.append(tempfile.TemporaryFile(prefix=filename+'.shuf', dir=path,mode='w+',encoding='utf8'))
    else:
        fds = [open(ff+'.shuf','w',encoding='utf8') for ff in files]

    for l in lines:
        s = l.strip().split('|||')
        for ii, fd in enumerate(fds):
            fd.write(s[ii]+'\n')
            #print (s[ii],file=fd)

    if temporary:
        [ff.seek(0) for ff in fds]
    else:
        [ff.close() for ff in fds]

    os.close(tf_os)
    os.remove(tpath)

    

    return fds

if __name__ == '__main__':
    main(sys.argv[1:])

    


