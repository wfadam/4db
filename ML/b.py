from math import sqrt
import time
import string
import re
import os
import getpass
import sys
import commands

user = getpass.getuser()


def sum(lst):
        rslt = 0
        for e in lst:
           rslt += e
        return rslt

def mean(lst):
    return sum(lst) / len(lst)

def stddev(lst):
    mn = mean(lst)
    variance = sum([(e-mn)**2 for e in lst]) / len(lst)
    return sqrt(variance)

def pin2val(dir):
	dict = {}
        fieldCut = re.compile("\s+");
        for dataFile in filter(lambda x: "-S0" in x, os.listdir(dir)):
                site = dataFile[-9:-4]
                dc_lines = filter(lambda line: re.search("^\s+-.*mV", line) , open(dir+dataFile).readlines())
                for field in map(lambda line: fieldCut.split(line), dc_lines):
			[val, pin, siteDut] = float(field[1][1:-4]), field[4], field[5]
                        key = "%s:%s:%s" % (site, siteDut, pin)
                        if key in dict:
                                dict[key].append(val)
                        else:
                                dict[key] = [val]
	return dict

def tdCount(dict):
	if len(dict) == 0:
		return 0
	orderedPinByTestCnt = sorted(dict, key = lambda x : len(dict[x])) #by ascending td
	return len(dict[orderedPinByTestCnt[-1]])

def perPinStat(dict):
        per_pin_stat = {}
        for key in dict:
                f_vals = map(lambda x: float(x[1:-4]), dict[key])
                per_pin_stat[key] = [max(f_vals), stddev(f_vals)]
        return per_pin_stat

def pin2stat(dict, func):
	skippedDuts = {}
        pin2stat = {}
        for key in dict:
		[site_n_dut, pin] = key.split(":PIN")
		if site_n_dut in skippedDuts:
			continue

		vals = dict[key]
		if len(vals) >= 3:
			pin2stat[key] = func(vals)
		else:
			skippedDuts[site_n_dut] = ""

	if len(skippedDuts) > 0:
		print "The following DUTs are ommited due to insufficient data:\n\t%s" % "\n\t".join(sorted(skippedDuts))

        return pin2stat

def copy(src, dst):
	for key in src:
		if key in dst:
			dst[key] = dst[key] + src[key]
		else:
			dst[key] = src[key]

p2vAll = {}
for idx, lot in enumerate(sys.argv[1:]):
        dir = "/home/%s/datalog/%s/" % (user, lot)

	pkg = commands.getoutput("grep -m 1 'Test Flow:' %s*S0001.txt | awk '{print $4}'" % dir)

        start = time.time()
	sys.stderr.write("(%d/%d) processing %s:%s " % (idx+1, len(sys.argv[1:]), pkg, lot));
        p2vLot = pin2val(dir)
	tdCnt = tdCount(p2vLot)
	copy(p2vLot, p2vAll)
        end = time.time()
        sys.stderr.write("(%dTD) takes %.3fs\n" % (tdCnt, end - start))

p2s = pin2stat(p2vAll, max)

dut2vec = {}
for key in p2s:
	[site_n_dut, pin] = key.split(":PIN")
	if site_n_dut in dut2vec:
		dut2vec[site_n_dut][pin] = p2s[key]
	else:
		dut2vec[site_n_dut] = {pin: p2s[key]}

for site_n_dut in dut2vec:
	vec = []
	orderedPin = sorted(dut2vec[site_n_dut], key = lambda pin: int(pin))
	for pin in orderedPin:
		vec.append(dut2vec[site_n_dut][pin])
	print "_%d, %s, %s" % (len(orderedPin), site_n_dut, str(orderedPin)[1:-1])
	print "%d, %s, %s" % (len(vec), site_n_dut, str(vec)[1:-1])


