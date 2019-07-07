# Andrew Lamont
# July 2019

def gen(input, change=False, insert=False, footing=False):
	# Returns a set of candidates from an input
	candidates = set([input])

	# a -> b ; b -> a
	if change:
		for i in range(len(input)):
			if input[i] == 'a':
				candidates.add(input[:i] + 'b' + input[i+1:])
			elif input[i] == 'b':
				candidates.add(input[:i] + 'a' + input[i+1:])

	# 0 -> a
	if insert:
		for i in range(len(input) + 1):
			candidates.add(input[:i] + 'a' + input[i:])

	# s -> (S) ; ss -> (SS)
	if footing:
		for i in range(len(input)):
			if input[i] == 's':
				candidates.add(input[:i] + '(S)' + input[i+1:])
		for i in range(len(input) - 1):
			if input[i] == input[i+1] == 's':
				candidates.add(input[:i] + '(SS)' + input[i+2:])

	return candidates

def eval(input, candidates, constraints):
	# Returns a set of optimal candidates
	tableau = []
	for can in candidates:
		row = [can]
		for con in (constraints):
			row.append(con(input, can))
		tableau.append(row)

#	print input
#	for row in tableau:
#		print row
#	print

	for i in range(1, len(constraints) + 1):
		vioset = set([])
		for r in range(len(tableau)):
			vioset.add(tableau[r][i])

		# Constraint decides
		if len(vioset) > 1:
			viomin = min(vioset)
			tableau = [r for r in tableau if r[i] == viomin]

#	print input
#	for row in tableau:
#		print row
#	print

	optima = [r[0] for r in tableau]
	return optima

# Constraint definitions
def ident(input, candidate):
	# IDENT
	if input == candidate:
		return 0
	if len(input) == len(candidate):
		return 1

def dep(input, candidate):
	# DEP
	if len(input) < len(candidate):
		return 1
	return 0

def starA(input, candidate):
	# *a
	vios = 0
	for i in range(len(candidate)):
		if candidate[i] == 'a':
			vios += 1
	return vios

def starAB(input, candidate):
	# *{ab, ba}
	vios = 0
	for i in range(len(candidate) - 1):
		if candidate[i] != candidate[i+1]:
			vios += 1
	return vios

def starAA(input, candidate):
	# *aa
	vios = 0
	for i in range(len(candidate) - 1):
		if candidate[i:i+2] == 'aa':
			vios += 1
	return vios

def starBBB(input, candidate):
	# *bbb
	vios = 0
	for i in range(len(candidate) - 2):
		if candidate[i:i+3] == 'bbb':
			vios += 1
	return vios

def FtBin(input, candidate):
	# FtBin
	vios = 0
	for i in range(len(candidate) - 2):
		if candidate[i:i+3] == '(S)':
			vios += 1
	return vios

def ParseSyl(input, candidate):
	# Parse-Syllable
	vios = 0
	for i in range(len(candidate)):
		if candidate[i] == 's':
			vios += 1
	return vios

# Convergent tie: *a >> IDENT
ur = 'aaaa'
outputs = set([])
stack = [ur]

while stack:
	input = stack.pop()
	candidates = gen(input, change=True)
	optima = eval(input, candidates, [starA, ident])
	for optimum in optima:
		if optimum == input:
			outputs.add(optimum)
		else:
			stack.append(optimum)

print '/' + ur + '/ -> [' + ', '.join(outputs) + ']'

# Divergent tie: *{ab, ba} >> IDENT
ur = 'ababa'
outputs = set([])
stack = [ur]

while stack:
	input = stack.pop()
	candidates = gen(input, change=True)
	optima = eval(input, candidates, [starAB, ident])
	for optimum in optima:
		if optimum == input:
			outputs.add(optimum)
		else:
			stack.append(optimum)

print '/' + ur + '/ -> [' + ', '.join(outputs) + ']'

# Divergent tie: *aa >> IDENT
ur = 'aaaaa'
outputs = set([])
stack = [ur]

while stack:
	input = stack.pop()
	candidates = gen(input, change=True)
	optima = eval(input, candidates, [starAA, ident])
	for optimum in optima:
		if optimum == input:
			outputs.add(optimum)
		else:
			stack.append(optimum)

print '/' + ur + '/ -> [' + ', '.join(outputs) + ']'

# Divergent tie: *bbb >> DEP
ur = 'bbbbbb'
outputs = set([])
stack = [ur]

while stack:
	input = stack.pop()
	candidates = gen(input, insert=True)
	optima = eval(input, candidates, [starBBB, dep])
	for optimum in optima:
		if optimum == input:
			outputs.add(optimum)
		else:
			stack.append(optimum)

print '/' + ur + '/ -> [' + ', '.join(outputs) + ']'

# Divergent tie: FtBin >> Parse-Syllable
ur = 'ssssss'
outputs = set([])
stack = [ur]

while stack:
	input = stack.pop()
	candidates = gen(input, footing=True)
	optima = eval(input, candidates, [FtBin, ParseSyl])
	for optimum in optima:
		if optimum == input:
			outputs.add(optimum)
		else:
			stack.append(optimum)

print '/' + ur + '/ -> [' + ', '.join(outputs) + ']'
