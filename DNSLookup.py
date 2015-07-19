import subprocess
import re
import os

def matchRTT(outValue):
    pattern = re.compile(r'Query.*msec')
    match=re.search(pattern, outValue)
    pattern = re.compile(r'\d+')
    match=re.search(pattern, match.group())
    return match.group()
    
localDnsServer = '202.120.2.101'
rttList = []
i=0
while i<100:
    hostname = 'www.' + ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(4)))+'.com'
    command = 'dig @' + localDnsServer + ' ' + hostname + ' +nocomments +noanswer +noquestion +noauthority +norecurse'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out,error = p.communicate()
    rtt = matchRTT(out)
    rttList.append(rtt)
    i = i+1
for rtt in rttList:
    print rtt
