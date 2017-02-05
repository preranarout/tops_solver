#!/usr/bin/env python
# Prerana Rout

import sys
import csv
from gurobipy import *

STATUS_OPTIMAL = 1
STATUS_INFEASIBLE = 0
STATUS_UNKNOWN = -1

OP_MAXIMIZE = -1
OP_MINIMIZE = 1

# Read LP problem from an lp file and returns the LP model in Gurobi model format
def read_lp(lp_filename_):	
	return read(lp_filename_)

# Write the LP problem to the filename specified
def write_lp(model, lp_filename_):
	model.write(lp_filename_)

# Check the type of optimization function, maximization or minimization
def lp_model_sense(model):
	if (model.ModelSense == OP_MAXIMIZE):
		print "Maximize"
	elif (model.ModelSense == OP_MINIMIZE):
		print "Minimize"

	return model.ModelSense

# Solve Gurobi linear expression with the input x_vector as variable values
def solveLinearExpression(linear_expr, x_vector):
	value = 0;
	value = value + linear_expr.getConstant()
	for i in range(0, linear_expr.size()):
		value = value + x_vector[i]*linear_expr.getCoeff(i)

	return value

def changeLinearExpressionSign(linear_expr):
	new_expr = LinExpr()	
	new_expr.addConstant(-linear_expr.getConstant())
	for i in range(0, linear_expr.size()):
		new_expr.add(linear_expr.getVar(i), -linear_expr.getCoeff(i))

	return new_expr

# LP variables as Gurobi Var type
def getVariables(model):
	return model.getVars()

# LP constraints as Gurobi Linear Expressions
def getConstraints(model):
	return model.getConstrs()

# LP Objective function as Gurobi Linear Expression
def getObjectiveFunction(model):
	return model.getObjective()

# Sets objective function of the Gurobi Model with the linear expression provided
def setObjectiveFunction(model, expr, op_type = OP_MAXIMIZE):
	if (op_type == OP_MAXIMIZE):
		model.setObjective(expr, GRB.MAXIMIZE)
	elif (op_type == OP_MINIMIZE):
		model.setObjective(expr, GRB.MINIMIZE)

# Updates the Gurobi Model to include all the previous changes
def updateModel(model):
	model.update()

# Performs the optimization and returns the result of optimization
def optimize(model):
	model.optimize()
	if (model.status == GRB.Status.INF_OR_UNBD):
		model.setParam(GRB.Param.Presolve, 0)
		model.optimize()	

	if (model.status == GRB.Status.OPTIMAL):
		return 1
	if (model.status == GRB.Status.INFEASIBLE):
		return 0
	else:
		return 1
