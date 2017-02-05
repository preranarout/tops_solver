#!/usr/bin/env python
# Prerana Rout

import sys
from gurobipy import *
import argparse
import copy
import os

import lp_helper as lph 	# Contains all Gurobi LP helper functions
import library_io as libio 	# Contains all csv and print Input/Output (IO) functions

optimal_lambda = None

# Page 22/23
# D(x), eqn. 3 and eqn. 4
# Computes the solution difference between two binary vectors x and y
def computeSolutionDifference(x, y, weights):
	if (len(x) != (len(y))):
		print 'Binary Vector sizes do not match.'
		return None

	D_x = 0
	for i in range(0, len(y)):
		if (y[i] == 0):
			D_x = D_x + x[i]*weights[i]
		elif (y[i] == 1):
			D_x = D_x + (1 - x[i])*weights[i]

	return D_x

# Page 23
# N(x), eqn. 5
# Takes inputs: objective function, x and y binary vectors and computes the quality improvement from y to x
# If op_type == -1, then maximize, if op_type == 1, then minimize
def qualityImprovement(obj_func, x, y, op_type = lph.OP_MAXIMIZE):
	cT_x = lph.solveLinearExpression(obj_func, x)
	cT_y = lph.solveLinearExpression(obj_func, y)
	if (op_type == -1):
		N_x = cT_x - cT_y
	elif (op_type == 1):
		N_x = cT_y - cT_x

	return N_x

# TODO: Comment properly
def DxLinearExpression(y, dink_model, weights):	
	# D(x) = |x - y|
	lp_variables = lph.getVariables(dink_model)
	expr = LinExpr()
	for i in range(0, len(y)):
		if (y[i] == 0):
			expr.add(lp_variables[i], weights[i])
		elif (y[i] == 1):
			expr.add(lp_variables[i], -weights[i])
			expr.addConstant(1*weights[i])	

	return expr

# If op_type == -1, then maximize, if op_type == 1, then minimize
def NxLinearExpression(y, dink_model, obj_func, op_type = lph.OP_MAXIMIZE):
	# N_x = cT_x - cT_y	
	# cT_x is the obj_func
	cT_y = lph.solveLinearExpression(obj_func, y)
	if (op_type == lph.OP_MAXIMIZE):
		cT_x = obj_func.copy()
		cT_x.addConstant(-cT_y)
	elif (op_type == lph.OP_MINIMIZE):
		cT_x = obj_func.copy()
		cT_x = lph.changeLinearExpressionSign(cT_x)		
		cT_x.addConstant(cT_y)

	return cT_x

# Page 24
# delta_q(x) = max N(x), eqn. 11
# Takes inputs: Quality improvement N(x)
def del_qx(N_x):
	del_qx.max_qx = -sys.maxint - 1
	if (N_x > del_qx.max_qx):
		del_qx.max_qx = N_x

	return del_qx.max_qx

# Page 25
# delta_s(x) = max D(x), eqn. 15
# Takes inputs: Solution Difference D(x)
def del_sx(D_x):
	del_sx.max_dx = -sys.maxint - 1
	if (D_x > del_sx.max_dx):
		del_sx.max_dx = D_x

	return del_sx.max_dx

# Page 25
# N = delta_s(x) / delta_q(x), eqn. 17
# Takes inputs: delta_s(x), delta_q(x)
def normalizationFactor(D_x, N_x):
	d_sx = del_sx(D_x)
	d_qx = del_qx(N_x)
	
	if (d_sx == d_qx):	# This is there to prevent division by zero when d_sx = d_qx = 0
		N = 1
	elif (d_qx == 0):
		d_qx = 0.00001
	else:
		N = d_sx / d_qx
	
	return N

# Dinkelbach Objective = N * N_x - lambda_ * D_x
def createDinkelbachObjective(D_x, N_x, N, lambda_):	
	return (N * N_x) - (lambda_ * D_x)

# Page 25, table 2, last row ... constraints
# c1_expr = D(x) >= deviation
# c2_expr = N(x) >= 0.001
def addDinkelbachConstraints(dink_model, c1_expr, c2_expr, deviation):
	# Is this where the Professor wants me to take the user's input as to 
	# how much should the deviation be from the original solution?
	# 1 means solution difference where at least 1 value is different, that is say x[13] is 0 in y (initial_values) and 1 in x (optimized values)
	# dink_model.addConstr(c1_expr, GRB.GREATER_EQUAL, deviation, "dc1")
	dink_model.addConstr(c1_expr, GRB.EQUAL, deviation, "dc1")
	#dink_model.addConstr(c1_expr, GRB.LESS_EQUAL, deviation, "dc1")
	dink_model.addConstr(c2_expr, GRB.GREATER_EQUAL, 0.001, "dc2")

	lph.updateModel(dink_model)

	# lph.write_lp(dink_model, 'infeasible_p0033/inf_10.lp')
	# exit(1)

# x_0 = initial solution vector
# weights = individual vector variable weights
# obj_func = objective function of lp_model
# dink_model = a copy of lp_model
# deviation = specifies the minimum deviation from the initial solution
# returns the optimized solution vector
def dinkelbach_solve(x_0, weights, obj_func, dink_model, deviation, op_type):
	global optimal_lambda

	y = x_0
	x_k = [0] * len(y)	
	epsilon = 0.000001
	x_ = None
	iteration_limit = 100;

	F_k = 0
	k = 0
	lambda_ = 0
	continue_flag = True
	while (continue_flag == True):
		D_x = computeSolutionDifference(x_k, y, weights)
		libio.pprint(libio.GREEN_TEXT, str(D_x))
		N_x = qualityImprovement(obj_func, x_k, y, op_type)
		libio.pprint(libio.GREEN_TEXT, str(N_x))
		N = normalizationFactor(D_x, N_x)		

		D_x = DxLinearExpression(y, dink_model, weights)
		N_x = NxLinearExpression(y, dink_model, obj_func, op_type)
		
		# Objective function:
		# 		max { N * N_x - lambda_ * D_x }
		objective_function = createDinkelbachObjective(D_x, N_x, N, lambda_)			# Dinkelbach d(x) <--- Created from f(x)
		lph.setObjectiveFunction(dink_model, objective_function, lph.OP_MAXIMIZE)

		if (k == 0):
			addDinkelbachConstraints(dink_model, D_x, N_x, deviation)	# TODO: N_x will be without weights

		# Optimize max { N * N_x - lambda_ * D_x }
		# dink_model.optimize()
		op_result = lph.optimize(dink_model)
		if (op_result == lph.STATUS_UNKNOWN):
			print 'Optimization failed.'
			return None
		elif (op_result == lph.STATUS_INFEASIBLE):
			print 'Optimization failed because model is infeasible.'
			return None

		F_k = abs(dink_model.objVal)				
		x_k = []
		for v in lph.getVariables(dink_model):
			x_k.append(v.x)				

		libio.pprint(libio.YELLOW_TEXT, '\n\nDebugging:')
		libio.pprint(libio.YELLOW_TEXT, '==========================================================')
		libio.pprint(libio.YELLOW_TEXT, ('|F_k|    : ' + str(F_k)))
		libio.pprint(libio.YELLOW_TEXT, ('Obj val  : ' + str(lph.solveLinearExpression(obj_func, x_k))))
		libio.pprint(libio.YELLOW_TEXT, ('Lambda   : ' + str(lambda_)))
		N_xk = qualityImprovement(obj_func, x_k, y, op_type)
		D_xk = computeSolutionDifference(x_k, y, weights)
		libio.pprint(libio.YELLOW_TEXT, ('N_xk     : ' + str(N_xk)))
		libio.pprint(libio.YELLOW_TEXT, ('D_xk     : ' + str(D_xk)))
		libio.pprint(libio.YELLOW_TEXT, ('Lambda*  : ' + str(N_xk / D_xk)))
		optimal_lambda = 'Optimal Lambda - ' + str(N_xk / D_xk)
		libio.pprint(libio.YELLOW_TEXT, '==========================================================\n\n')

		if (F_k <= epsilon):
			x_ = x_k
			continue_flag = False
		elif (k >= (iteration_limit - 1)):
			x_ = x_k
			continue_flag = False
		else:
			N_xk = qualityImprovement(obj_func, x_k, y, op_type)
			D_xk = computeSolutionDifference(x_k, y, weights)	
			lambda_ = (N * N_xk) / D_xk
			k = k + 1

	if (x_ == None):
		libio.pprint(libio.RED_TEXT, 'Could not find solution.')
		return None
	elif (k >= (iteration_limit - 1)):
		libio.pprint(libio.YELLOW_TEXT, 'Iteration limit.')

	return x_

# Makes a deep copy of the lp_model
def createDinkelbachModel(initial_model):
	dink_model = initial_model.copy()	
	return dink_model

def main_function():
	global optimal_lambda
	
	parser = argparse.ArgumentParser(description='Dinkelbach algorithm to solve modified BIP.')
	parser.add_argument("-i", "--init", metavar=('<csv file>'), help='user provided initial values (.csv file)')
	parser.add_argument('-l', '--lp', metavar=('<lp file>'), help='path to lp file (.lp file)')
	parser.add_argument('-m', '--mps', metavar=('<mps file>'), help='path to mps file (.mps file)')
	parser.add_argument('-d', '--deviation', metavar=('<value>'), type=float, help='min percentage deviation of the optimum solution (Float)')
	parser.add_argument('-w', '--weights', metavar=('<csv file>'), help='user provided variable weights (.csv file)')
	parser.add_argument('-s', '--status_quo', help="Invert max/min type and generate status_quo vector", action="store_true")

	args = parser.parse_args()

	init_csv_filename = args.init
	lp_filename = args.lp
	mps_filename = args.mps
	deviation_percentage = args.deviation
	weights_filename = args.weights
	status_quo_only = args.status_quo

	print("ASFAF")

	# print os.getcwd()
	os.chdir('C:\Users\user\Desktop\dinkelbach_algorithm_bip')
	print os.getcwd()

	if (status_quo_only == False):
		if (init_csv_filename == None):		
			init_csv_filename = 'user_initial_files/user_initial_gap_1.csv'
			libio.pprint(libio.YELLOW_TEXT, 'CSV filename not specified. Using default initial values from \"user_initial.csv\" See help at \"dinkelbach.py --help\".')

	if (mps_filename != None):
		lp_filename = mps_filename

	if (lp_filename == None):
		lp_filename = 'gap_files/gap1.lp'
		libio.pprint(libio.YELLOW_TEXT, 'LP filename not specified. Using default LP problem from \"gap1.lp\". See help at \"dinkelbach.py --help\".')	
	
	if (deviation_percentage == None):
		deviation_percentage = 10.0
		libio.pprint(libio.YELLOW_TEXT, 'Deviation percentage not specified. Using default of 10.0. See help at \"dinkelbach.py --help\"')
	else:
		deviation_percentage = float(deviation_percentage)

	if ((deviation_percentage < 0.0) or (deviation_percentage > 100.0)):
		libio.pprint(libio.RED_TEXT, 'Deviation percentage should be between 0.0 and 100.0. Please give a valid value. Exiting program.')
		exit(-1)

	if (weights_filename == None):
		weights = []
		libio.pprint(libio.YELLOW_TEXT, 'Weights not specified. Using default of ( num_variables * [ 1 ] ). See help at \"dinkelbach.py --help\"')
	else:
		weights_file = libio.read_csv(weights_filename)
		weights = libio.csv_to_1d_list(weights_file)

	# Declare all the main function vars here so that it is easy to see all the vars in use
	csv_file 			= None
	lp_model 			= None
	lp_variables 		= None
	# lp_constraints 		= None
	lp_objective_func 	= None

	if (status_quo_only == False):
		csv_file 			= libio.read_csv(init_csv_filename)
		initial_values 		= libio.csv_to_1d_list(csv_file)	
	lp_model 			= lph.read_lp(lp_filename)
	lp_variables 		= lph.getVariables(lp_model)
	# lp_constraints 		= lph.getConstraints(lp_model)	
	dink_model 			= createDinkelbachModel(lp_model)		
	lp_objective_func 	= lph.getObjectiveFunction(dink_model)	

	problem_type = lph.lp_model_sense(lp_model)

	# Generate status_quo if flag enabled
	if (status_quo_only == True):
		objective_function = lph.getObjectiveFunction(lp_model)
		if (lp_model.ModelSense == lph.OP_MAXIMIZE):
			lph.setObjectiveFunction(lp_model, objective_function, lph.OP_MINIMIZE)
		else:
			lph.setObjectiveFunction(lp_model, objective_function, lph.OP_MAXIMIZE)

	# Gives the best possible solution without taking into account solution difference or anything, just for reference
	op_result = lph.optimize(lp_model)
	if (op_result == lph.STATUS_UNKNOWN):
		print 'Optimization failed.'
		return None
	elif (op_result == lph.STATUS_INFEASIBLE):
		print 'Optimization failed because model is infeasible.'
		return None

	# Putting the best possible solution values from lp_model.optimize() into x_k vector after converting them to integers for printing out at the end
	x_k = []
	for v in lph.getVariables(lp_model):
		x_k.append(int(v.x))

	# Print the status_quo value and exit
	if (status_quo_only == True):
		print "STATUS QUO VALUE: "
		print x_k
		exit(0)

	weights = [1] * len(x_k)
		
	max_deviation = computeSolutionDifference(x_k, initial_values, weights)

	# Convert deviation percentage to deviation in terms of the number of variables	
	# deviation = int(len(lp_variables) * deviation_percentage / 100)
	deviation = int(max_deviation * deviation_percentage / 100)

	libio.pprint(libio.GREEN_TEXT, str(deviation))

	# Dinkelbach solution
	solution = dinkelbach_solve(initial_values, weights, lp_objective_func, dink_model, deviation, problem_type)
	
	# Converting solution vector of floats (decimals) to integer so that it looks better when printed out
	int_solution = []
	if (solution != None):
		for v in solution:
			int_solution.append(int(v))
	
	print "GAP FILE: ", str(lp_filename)	

	if (problem_type == lph.OP_MAXIMIZE):
		libio.pprint(libio.GREEN_TEXT, '\nOptimization type: MAXIMIZE\n')
	elif (problem_type == lph.OP_MINIMIZE):
		libio.pprint(libio.GREEN_TEXT, '\nOptimization type: MINIMIZE\n')
	else:
		libio.pprint(libio.RED_TEXT, '\nError: Optimization type unknown\n')

	print 'Initial objective function value                 :', lph.solveLinearExpression(lp_objective_func, initial_values)
	if (solution != None):
		if (problem_type == lph.OP_MAXIMIZE):
			libio.pprint(libio.GREEN_TEXT, ('\nDinkelbach solution max objective function value : ' + str(lph.solveLinearExpression(lp_objective_func, solution))))
		elif (problem_type == lph.OP_MINIMIZE):
			libio.pprint(libio.GREEN_TEXT, ('\nDinkelbach solution min objective function value : ' + str(lph.solveLinearExpression(lp_objective_func, solution))))
	if (problem_type == lph.OP_MAXIMIZE):
		print '\nMax possible objective function value            :', lp_model.objVal
	elif (problem_type == lph.OP_MINIMIZE):
		print '\nMin possible objective function value            :', lp_model.objVal
	
	# print '\nInitial solution vector provided (', init_csv_filename, '): '
	# print initial_values
	# if (solution != None):
		# libio.pprint(libio.GREEN_TEXT, ('\nDinkelbach Solution vector       :\n' + str(int_solution)))
	# print '\nBest possible solution vector    : '
	# print x_k

	print '\nDeviation percentage             : ', deviation_percentage, '%'
	print 'Minimum Deviation                : ', deviation
	if (solution != None):
		print 'Solution Deviation               : ', computeSolutionDifference(solution, initial_values, weights)

	if (solution == None):
		libio.pprint(libio.RED_TEXT, '\nDinkelbach: OPTIMIZATION FAILED as either the model is infeasible or parameters were not correct. Please review the problem provided.\n')
	else:
		libio.pprint(libio.GREEN_TEXT, '\nDinkelbach: Solution found.\n')

	print optimal_lambda

if __name__ == "__main__":
	main_function()