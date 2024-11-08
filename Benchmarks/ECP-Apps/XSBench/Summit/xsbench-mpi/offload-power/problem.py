import numpy as np
from numpy import abs, cos, exp, mean, pi, prod, sin, sqrt, sum
from autotune import TuningProblem
from autotune.space import *
import os
import sys
import time
import json
import math

import ConfigSpace as CS
import ConfigSpace.hyperparameters as CSH
from skopt.space import Real, Integer, Categorical

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.dirname(HERE)+ '/plopper')
from plopper import Plopper

cs = CS.ConfigurationSpace(seed=1234)
# number of threads (x4 for smt4)
p0= CSH.OrdinalHyperparameter(name='p0', sequence=['8','10','16','21','32','42'], default_value='42')
# omp placement
p1= CSH.CategoricalHyperparameter(name='p1', choices=['cores','threads','sockets'], default_value='cores')
# OMP_PROC_BIND
p2= CSH.CategoricalHyperparameter(name='p2', choices=['close','spread','master'], default_value='close')
#omp parallel
p3= CSH.CategoricalHyperparameter(name='p3', choices=["#pragma omp parallel for", " "], default_value=' ')
#omp parallel simd
p4= CSH.CategoricalHyperparameter(name='p4', choices=["simd", " "], default_value=' ')
#omp target device selected
p5= CSH.CategoricalHyperparameter(name='p5', choices=["device(offloaded_to_device)", " "], default_value=' ')
# OMP_SCHEDULE
p6= CSH.CategoricalHyperparameter(name='p6', choices=['dynamic','static','auto'], default_value='static')
#omp target schedule
p7= CSH.CategoricalHyperparameter(name='p7', choices=["schedule(static,1)", " "], default_value=' ')
#OMP_TARGET_OFFLOAD
p8= CSH.CategoricalHyperparameter(name='p8', choices=['DEFAULT','DISABLED','MANDATORY'], default_value='DEFAULT')
#MPI Barrier
p9= CSH.CategoricalHyperparameter(name='p9', choices=['MPI_Barrier(MPI_COMM_WORLD);',' '], default_value='MPI_Barrier(MPI_COMM_WORLD);')

cs.add_hyperparameters([p0, p1, p2, p3, p4, p5, p6, p7, p8, p9])

# problem space
task_space = None

input_space = cs

output_space = Space([
     Real(0.0, inf, name="time")
])

dir_path = os.path.dirname(os.path.realpath(__file__))
kernel_idx = dir_path.rfind('/')
kernel = dir_path[kernel_idx+1:]
obj = Plopper(dir_path+'/mmp.c',dir_path)

x1=['p0','p1','p2','p3','p4','p5','p6','p7','p8','p9']

def myobj(point: dict):

  def plopper_func(x):
    x = np.asarray_chkfinite(x)  # ValueError if any NaN or Inf
    value = [point[x1[0]],point[x1[1]],point[x1[2]],point[x1[3]],point[x1[4]],point[x1[5]],point[x1[6]],point[x1[7]],point[x1[8]],point[x1[9]]]
    x11 = int(point[x1[0]])
    x111 = x11 * 4
    print('VALUES: ', x111)
    #os.environ["OMP_NUM_THREADS"] = str(x111)
    os.system("processexe.pl exe.pl " +point[x1[0]])
    #print('VALUES: 4x',point[x1[0]])
    params = ["P0","P1","P2","P3","P4","P5","P6","P7","P8","P9"]

    result = obj.findRuntime(value, params)
    return result

  x = np.array([point[f'p{i}'] for i in range(len(point))])
  results = plopper_func(x)
  print('OUTPUT:%f',results)

  return results

Problem = TuningProblem(
    task_space=None,
    input_space=input_space,
    output_space=output_space,
    objective=myobj,
    constraints=None,
    model=None
    )
