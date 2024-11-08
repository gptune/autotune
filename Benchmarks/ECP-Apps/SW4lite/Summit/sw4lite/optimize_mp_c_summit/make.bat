module load netlib-lapack
mpif90 -O3 -fopenmp -c ../src/type_defs.f90
mpic++ -O3 -I../src -fopenmp -DSW4_OPENMP -DSW4_CROUTINES -DSW4_CROUTINES  -I../src/double -o sw4lite ../src/main.C ../src/EW.C ../src/Sarray.C ../src/Source.C ../src/SuperGrid.C ../src/GridPointSource.C ../src/time_functions.C ../src/EW_cuda.C ../src/ew-cfromfort.C ../src/EWCuda.C ../src/CheckPoint.C ../src/Parallel_IO.C ../src/EW-dg.C ../src/MaterialData.C ../src/MaterialBlock.C ../src/Polynomial.C ../src/SecondOrderSection.C ../src/Filter.C ../src/TimeSeries.C ../src/sacsubc.C ../src/curvilinear-c.C -llapack
