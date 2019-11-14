import sys
f = open(sys.argv[1], "r")
for line in f.readlines():
	fields = line.split()
	dut = fields[2]
	vals = map(lambda sVal : int(sVal, 16)*1.0, fields[5:])
	print "%s, %s" % (dut, ", ".join(str(s) for s in vals))
