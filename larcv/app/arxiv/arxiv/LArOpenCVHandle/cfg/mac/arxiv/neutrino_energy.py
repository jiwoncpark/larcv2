import pandas as pd
import numpy as np
import sys
from util.good_vertex import retrieve_events
from util.util import energy_plotter

INFILE = sys.argv[1]

ret=retrieve_events(INFILE)

signal_df_m=ret["signal_df_m"]
sig_good_vtx_df=ret["sig_good_vtx_df"]
base_index=ret["base_index"]

sig_mctree_s=signal_df_m["MCTree"]
sig_mctree_t=signal_df_m["MCTree"].ix[sig_good_vtx_df.reset_index().set_index(base_index).index]

Emin=0#200
Emax=3000#600
deltaE=50

energy_plotter(sig_mctree_s,
               sig_mctree_t,
               Emin,
               Emax,
               deltaE,
               'energyInit',
               'Neutrino True')
