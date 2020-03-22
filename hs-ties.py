# Andrew Lamont
# March 2020

def gen(input, change=False, insert=False, footing=False, metathesis=False):
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

	# xy -> yx
	if metathesis:
		for i in range(len(input) - 1):
			candidates.add(input[:i] + input[i+1] + input[i] + input[i+2:])

	return candidates

def eval(input, candidates, constraints):
	# Returns a set of optimal candidates
	tableau = []
	for can in candidates:
		row = [can]
		for con in (constraints):
			if con.type == 'faithfulness':
				row.append(con.vios(can, input))
			else:
				row.append(con.vios(can))
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

class Constraint:
	def __init__(self, name, loci=[]):
		self.name = name
		if self.name in ['ident', 'dep', 'contig']:
			self.type = 'faithfulness'
		else:
			self.type = 'markedness'
			self.loci = loci

	def vios(self, candidate, input=''):
		if self.type == 'faithfulness':
			if input == candidate:
				return 0
			if self.name == 'dep':
				if len(input) < len(candidate):
					return 1
			elif self.name == 'ident':
				if len(input) == len(candidate):
					return 1
			elif self.name == 'contig':
				for i in range(len(input) - 1):
					if input[i] == candidate[i+1] and input[i+1] == candidate[i]:
						return 1
		else:
			vios = 0
			for locus in self.loci:
				for i in range(len(candidate) + 1 - len(locus)):
					if candidate[i:i+len(locus)] == locus:
						vios += 1
			return vios

# Convergent tie: *a >> IDENT
ur = 'aaaa'
outputs = set([])
stack = [ur]

while stack:
	input = stack.pop()
	candidates = gen(input, change=True)
	optima = eval(input, candidates, [Constraint('*a', ['a']), Constraint('ident')])
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
	optima = eval(input, candidates, [Constraint('*ab', ['ab', 'ba']), Constraint('ident')])
	for optimum in optima:
		if optimum == input:
			outputs.add(optimum)
		else:
			stack.append(optimum)

print '/' + ur + '/ -> [' + ', '.join(outputs) + ']'

# Divergent tie: *{ab, ba} >> IDENT
ur = 'ababababa'
outputs = set([])
stack = [ur]

while stack:
	input = stack.pop()
	candidates = gen(input, change=True)
	optima = eval(input, candidates, [Constraint('*ab', ['ab', 'ba']), Constraint('ident')])
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
	optima = eval(input, candidates, [Constraint('*aa', ['aa']), Constraint('ident')])
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
	optima = eval(input, candidates, [Constraint('*bbb', ['bbb']), Constraint('dep')])
	for optimum in optima:
		if optimum == input:
			outputs.add(optimum)
		else:
			stack.append(optimum)

print '/' + ur + '/ -> [' + ', '.join(outputs) + ']'


# Divergent tie: *aba >> CONTIG
ur = 'abababa'
outputs = set([])
stack = [ur]

while stack:
	input = stack.pop()
	candidates = gen(input, metathesis=True)
	optima = eval(input, candidates, [Constraint('*aba', ['aba']), Constraint('contig')])
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
	optima = eval(input, candidates, [Constraint('FtBin',['(S)']), Constraint('ParseSyl', ['s'])])
	for optimum in optima:
		if optimum == input:
			outputs.add(optimum)
		else:
			stack.append(optimum)

print '/' + ur + '/ -> [' + ', '.join(outputs) + ']'

# Divergent tie: *bb >> *a >> IDENT
ur = 'aaaaa'
outputs = set([])
stack = [ur]

while stack:
	input = stack.pop()
	candidates = gen(input, change=True)
	optima = eval(input, candidates, [Constraint('*bb', ['bb']), Constraint('*a', ['a']), Constraint('ident')])
	for optimum in optima:
		if optimum == input:
			outputs.add(optimum)
		else:
			stack.append(optimum)

print '/' + ur + '/ -> [' + ', '.join(outputs) + ']'
