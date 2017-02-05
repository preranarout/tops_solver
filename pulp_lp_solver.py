# from pulp import *
import pulp

def testProblem():
	print("Running test problem -")
	x1 = pulp.LpVariable("x1", None, None, "Binary")
	# x1 = LpVariable("x1", 0, 40)
	x2 = pulp.LpVariable("x2", cat="Binary")
	# x2 = LpVariable("x2", 0, 1000)

	prob = pulp.LpProblem("lp_problem", pulp.LpMaximize)

	prob += 2*x1 + x2 <= 100 
	prob += x1 + x2 <= 80
	prob += x1 <= 40
	prob += x1 >= 0
	prob += x2 >= 0

	prob += 3*x1 + 2*x2

	# solve the problem
	status = prob.solve()
	pulp.LpStatus[status]

	# print the results x1 = 20, x2 = 60
	print "x1 = ", pulp.value(x1)
	print "x2 = ", pulp.value(x2)

def gap1():
	x = [0] 	# Variables vector
	for i in range(1, 76):
		var_name = "x" + str(i)
		x.append(pulp.LpVariable(var_name, cat="Binary"))

	prob = pulp.LpProblem("gap1", pulp.LpMaximize)

	# Constraints (equality)
	prob += x[1] + x[16] + x[31] + x[46] + x[61] == 1
	prob += x[2] + x[17] + x[32] + x[47] + x[62] == 1
	prob += x[3] + x[18] + x[33] + x[48] + x[63] == 1
	prob += x[4] + x[19] + x[34] + x[49] + x[64] == 1
	prob += x[5] + x[20] + x[35] + x[50] + x[65] == 1
	prob += x[6] + x[21] + x[36] + x[51] + x[66] == 1
	prob += x[7] + x[22] + x[37] + x[52] + x[67] == 1
	prob += x[8] + x[23] + x[38] + x[53] + x[68] == 1
	prob += x[9] + x[24] + x[39] + x[54] + x[69] == 1
	prob += x[10] + x[25] + x[40] + x[55] + x[70] == 1
	prob += x[11] + x[26] + x[41] + x[56] + x[71] == 1
	prob += x[12] + x[27] + x[42] + x[57] + x[72] == 1
	prob += x[13] + x[28] + x[43] + x[58] + x[73] == 1
	prob += x[14] + x[29] + x[44] + x[59] + x[74] == 1
	prob += x[15] + x[30] + x[45] + x[60] + x[75] == 1

	# Constraints (inequality)
	prob += 8 * x[1] + 15 * x[2] + 14 * x[3] + 23 * x[4] + 8 * x[5] + 16 * x[6] + 8 * x[7] + 25 * x[8] + 9 * x[9] + 17 * x[10] + 25 * x[11] + 15 * x[12] + 10 * x[13] + 8 * x[14] + 24 * x[15] <= 36
	prob += 15 * x[16] + 7 * x[17] + 23 * x[18] + 22 * x[19] + 11 * x[20] + 11 * x[21] + 12 * x[22] + 10 * x[23] + 17 * x[24] + 16 * x[25] + 7 * x[26] + 16 * x[27] + 10 * x[28] + 18 * x[29] + 22 * x[30] <= 34
	prob += 21 * x[31] + 20 * x[32] + 6 * x[33] + 22 * x[34] + 24 * x[35] + 10 * x[36] + 24 * x[37] + 9 * x[38] + 21 * x[39] + 14 * x[40] + 11 * x[41] + 14 * x[42] + 11 * x[43] + 19 * x[44] + 16 * x[45] <= 38
	prob += 20 * x[46] + 11 * x[47] + 8 * x[48] + 14 * x[49] + 9 * x[50] + 5 * x[51] + 6 * x[52] + 19 * x[53] + 19 * x[54] + 7 * x[55] + 6 * x[56] + 6 * x[57] + 13 * x[58] + 9 * x[59] + 18 * x[60] <= 27
	prob += 8 * x[61] + 13 * x[62] + 13 * x[63] + 13 * x[64] + 10 * x[65] + 20 * x[66] + 25 * x[67] + 16 * x[68] + 16 * x[69] + 17 * x[70] + 10 * x[71] + 10 * x[72] + 5 * x[73] + 12 * x[74] + 23 * x[75] <= 33

	prob += 17 * x[1] + 21 * x[2] + 22 * x[3] + 18 * x[4] + 24 * x[5] + 15 * x[6] + 20 * x[7] + 18 * x[8] + 19 * x[9] + 18 * x[10] + 16 * x[11] + 22 * x[12] + 24 * x[13] + 24 * x[14] + 16 * x[15] + 23 * x[16] + 16 * x[17] + 21 * x[18] + 16 * x[19] + 17 * x[20] + 16 * x[21] + 19 * x[22] + 25 * x[23] + 18 * x[24] + 21 * x[25] + 17 * x[26] + 15 * x[27] + 25 * x[28] + 17 * x[29] + 24 * x[30] + 16 * x[31] + 20 * x[32] + 16 * x[33] + 25 * x[34] + 24 * x[35] + 16 * x[36] + 17 * x[37] + 19 * x[38] + 19 * x[39] + 18 * x[40] + 20 * x[41] + 16 * x[42] + 17 * x[43] + 21 * x[44] + 24 * x[45] + 19 * x[46] + 19 * x[47] + 22 * x[48] + 22 * x[49] + 20 * x[50] + 16 * x[51] + 19 * x[52] + 17 * x[53] + 21 * x[54] + 19 * x[55] + 25 * x[56] + 23 * x[57] + 25 * x[58] + 25 * x[59] + 25 * x[60] + 18 * x[61] + 19 * x[62] + 15 * x[63] + 15 * x[64] + 21 * x[65] + 25 * x[66] + 16 * x[67] + 16 * x[68] + 23 * x[69] + 15 * x[70] + 22 * x[71] + 17 * x[72] + 19 * x[73] + 22 * x[74] + 24 * x[75]

	status = prob.solve()
	print (pulp.LpStatus[status])

	sol_vec = []
	for i in range(1, len(x)):
		sol_vec.append(int(pulp.value(x[i])))

	print sol_vec

	y = 17 * pulp.value(x[1]) + 21 * pulp.value(x[2]) + 22 * pulp.value(x[3]) + 18 * pulp.value(x[4]) + 24 * pulp.value(x[5]) + 15 * pulp.value(x[6]) + 20 * pulp.value(x[7]) + 18 * pulp.value(x[8]) + 19 * pulp.value(x[9]) + 18 * pulp.value(x[10]) + 16 * pulp.value(x[11]) + 22 * pulp.value(x[12]) + 24 * pulp.value(x[13]) + 24 * pulp.value(x[14]) + 16 * pulp.value(x[15]) + 23 * pulp.value(x[16]) + 16 * pulp.value(x[17]) + 21 * pulp.value(x[18]) + 16 * pulp.value(x[19]) + 17 * pulp.value(x[20]) + 16 * pulp.value(x[21]) + 19 * pulp.value(x[22]) + 25 * pulp.value(x[23]) + 18 * pulp.value(x[24]) + 21 * pulp.value(x[25]) + 17 * pulp.value(x[26]) + 15 * pulp.value(x[27]) + 25 * pulp.value(x[28]) + 17 * pulp.value(x[29]) + 24 * pulp.value(x[30]) + 16 * pulp.value(x[31]) + 20 * pulp.value(x[32]) + 16 * pulp.value(x[33]) + 25 * pulp.value(x[34]) + 24 * pulp.value(x[35]) + 16 * pulp.value(x[36]) + 17 * pulp.value(x[37]) + 19 * pulp.value(x[38]) + 19 * pulp.value(x[39]) + 18 * pulp.value(x[40]) + 20 * pulp.value(x[41]) + 16 * pulp.value(x[42]) + 17 * pulp.value(x[43]) + 21 * pulp.value(x[44]) + 24 * pulp.value(x[45]) + 19 * pulp.value(x[46]) + 19 * pulp.value(x[47]) + 22 * pulp.value(x[48]) + 22 * pulp.value(x[49]) + 20 * pulp.value(x[50]) + 16 * pulp.value(x[51]) + 19 * pulp.value(x[52]) + 17 * pulp.value(x[53]) + 21 * pulp.value(x[54]) + 19 * pulp.value(x[55]) + 25 * pulp.value(x[56]) + 23 * pulp.value(x[57]) + 25 * pulp.value(x[58]) + 25 * pulp.value(x[59]) + 25 * pulp.value(x[60]) + 18 * pulp.value(x[61]) + 19 * pulp.value(x[62]) + 15 * pulp.value(x[63]) + 15 * pulp.value(x[64]) + 21 * pulp.value(x[65]) + 25 * pulp.value(x[66]) + 16 * pulp.value(x[67]) + 16 * pulp.value(x[68]) + 23 * pulp.value(x[69]) + 15 * pulp.value(x[70]) + 22 * pulp.value(x[71]) + 17 * pulp.value(x[72]) + 19 * pulp.value(x[73]) + 22 * pulp.value(x[74]) + 24 * pulp.value(x[75])
	print ("\nMax value: " + str(y))

def main():
	# testProblem()
	gap1()

if __name__ == "__main__":
	main()