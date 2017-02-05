import pymprog

def main():
    problem = pymprog.glpk.glp_create_prob()
    pymprog.glpk.glp_read_lp(problem, None, "C:\Users\user\Desktop\dinkelbach_algorithm_bip\gap1.lp")
    pymprog.glpk.glp_exact(problem, None)
    # pymprog.glpk.glp_simplex(problem, None)
    # pymprog.glpk.glp_interior(problem, None)
    pymprog.glpk.glp_intopt(problem, None)

    # print pymprog.glpk.glp_get_obj_val(problem)
    print pymprog.glpk.glp_mip_obj_val(problem)

if __name__ == "__main__":
    main()