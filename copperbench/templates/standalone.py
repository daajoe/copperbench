#!/usr/bin/env python
import atexit
import subprocess
from multiprocessing import Pool, Process
#TODO: include core_pinning, multiprocess handling
#https://github.com/daajoe/reprobench/blob/jkf_wip_pnode/reprobench/core/worker.py
#TODO: include setting to base_frequency
import pathlib
from subprocess import Popen, PIPE
import time
from tqdm import tqdm

num_workers = 1
#num_workers = int(subprocess.check_output('cat /proc/cpuinfo | grep "physical id" | sort -u | wc -l',shell=True))
#isunix = (platform == "linux" or platform == "linux2")

startlist = []
with open('start_list.txt') as fh:
    for task in fh.readlines():
        if task == '':
            continue
        task=task.split('\n')[0]
        startlist.append(task)

num_pending=len(startlist)
#pool = Pool(num_workers)
#pool_iterator = pool.imap_unordered(self.spawn_worker, jobs_address)
#for _ in pool_iterator:
#    progress_bar.update()


cwd = str(pathlib.Path.cwd())
progress_bar = tqdm(desc="Executing runs", total=num_pending)

with open('standalone_stdout.txt','w') as fh_stdout:
    with open('standalone_stderr.txt', 'w') as fh_stderr:
        for cmd in startlist:
            print(f'Executing run "{cmd}"...')
            p_stats = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, close_fds=True, cwd=cwd)
            output, err = p_stats.communicate()
            fh_stdout.write('='*20 + cmd + '='*20 + '\n')
            fh_stderr.write('='*20 + cmd + '='*20 + '\n')
            fh_stdout.write(str(output.decode('utf8')))
            fh_stderr.write(str(err.decode('utf8')))
            fh_stdout.write('='*80 + '\n')
            fh_stderr.write('='*80 + '\n')
            progress_bar.update()
progress_bar.close()
#pool.close()
