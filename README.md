# tops_solver
Python code to solve a Binary Integer Programming problem using Dinkelbach's algorithm. Uses Gurobi.

usage: tops.py [-h] [-i <csv file>] [-l <lp file>] [-m <mps file>]
               [-d <value>] [-w <csv file>] [-s]

Dinkelbach algorithm to solve modified BIP.

optional arguments:
  -h, --help            show this help message and exit
  -i <csv file>, --init <csv file>
                        user provided initial values (.csv file)
  -l <lp file>, --lp <lp file>
                        path to lp file (.lp file)
  -m <mps file>, --mps <mps file>
                        path to mps file (.mps file)
  -d <value>, --deviation <value>
                        min percentage deviation of the optimum solution
                        (Float)
  -w <csv file>, --weights <csv file>
                        user provided variable weights (.csv file)
  -s, --status_quo      Invert max/min type and generate status_quo vector
