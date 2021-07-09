import math

def entropy(pos, neg):
	pos_prob = float(pos)/float(pos+neg)
	neg_prob = float(neg)/float(pos+neg)

	if pos_prob == 0:
		term1 = 0
	else:
		term1 = -pos_prob * math.log(pos_prob,2.0)

	if neg_prob == 0:
		term2 = 0
	else:
		term2 = -neg_prob *math.log(neg_prob, 2.0)

	value = term1 + term2

	return value

#test
print(entropy(2,2))
print(entropy(2,1))
print(entropy(1,0)) 