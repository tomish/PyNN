#!/usr/bin/env python

import subprocess, glob, os, sys

default_simulators = ['PCSIM', 'NEST', 'NEURON', 'Brian']
simulator_names = sys.argv[1:]
if len(simulator_names) > 0:
    for name in simulator_names:
        if name not in default_simulators:
            print "Simulator must be one of:", ", ".join(default_simulators)
            sys.exit(1)
else:
    simulator_names = default_simulators

simulators = []
for simulator in simulator_names:
    sim = simulator.lower()
    try:
        exec("import pyNN.%s" % sim)
        simulators.append(sim)
    except ImportError:
        pass

exclude = {
    'PCSIM': ("brunel.py", "HH_cond_exp.py", "EIF_cond_alpha_isfa_ista.py", "VAbenchmarks2-csa.py", "nineml_neuron.py"),
    'NEURON': ["VAbenchmarks2-csa.py", "nineml_neuron.py"],
    'NEST': ["VAbenchmarks2-csa.py", "nineml_neuron.py"],
    'Brian': ["VAbenchmarks2-csa.py", "nineml_neuron.py"],
}

extra_args = {
    "VAbenchmarks.py": "CUBA",
    "VAbenchmarks2.py": "CUBA",
    "VAbenchmarks2-csa.py": "CUBA",
    "VAbenchmarks3.py": "CUBA",
}

if not os.path.exists("Results"):
    os.mkdir("Results")

for simulator in simulator_names:
    if simulator.lower() in simulators:
        print "\n\n\n================== Running examples with %s =================\n" % simulator
        for script in glob.glob("../*.py"):
            script_name = os.path.basename(script)
            if script_name not in exclude[simulator]:
                cmd = "python %s %s" % (script, simulator.lower())
                if script_name in extra_args:
                    cmd += " " + extra_args[script_name]
                print cmd,
                sys.stdout.flush()
                logfile = open("Results/%s_%s.log" % (os.path.basename(script), simulator), 'w')
                p = subprocess.Popen(cmd, shell=True, stdout=logfile, stderr=subprocess.PIPE, close_fds=True)
                retval = p.wait()
                print retval == 0 and " - ok" or " - fail"
    else:
        print "\n\n\n================== %s not available =================\n" % simulator

print "\n\n\n================== Plotting results =================\n"
for script in glob.glob("../*.py"):
    cmd = "python plot_results.py %s" % os.path.basename(script)[:-3]
    print cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    p.wait()
