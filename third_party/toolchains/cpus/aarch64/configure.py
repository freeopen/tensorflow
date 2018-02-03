#!/usr/bin/env python3

import configparser
import readline
import glob
import sys
import os

def path_completer(text, state):
    matches = sorted([x for x in glob.glob(text + '*')])
    matches = [match if not os.path.isdir(match) else match+'/' for match in matches]
    return matches[state]

readline.set_completer_delims('\t')
readline.parse_and_bind("tab: complete")

readline.set_completer(path_completer)
while True:
    python_inc_dir = input("What is the target-side Python include directory? ")
    if not os.path.exists(python_inc_dir):
        print('The path does not exist.')
        continue
    break

readline.set_completer(None)
while True:
    is_cuda = input("Is it a CUDA build? (yes/no) ")
    if is_cuda not in ['no', 'yes']:
        print('Invalid answer.')
        continue
    break

cuda_dir = '/cuda/dir/not/specified'
cudnn_dir = '/cudnn/dir/not/specified'
if is_cuda == 'yes':
    readline.set_completer(path_completer)
    while True:
        cuda_dir = input("What is the CUDA installation directory? ")
        if not os.path.exists(cuda_dir):
            print('The path does not exist.')
            continue
        break

    readline.set_completer(path_completer)
    while True:
        cudnn_dir = input("What is the host-side cuDNN installation directory? ")
        if not os.path.exists(cudnn_dir):
            print('The path does not exist.')
            continue
        break

print('-----')
print('Configuring for:')
print('Target Python include directory:', python_inc_dir)
print('CUDA:', is_cuda)
if is_cuda == 'yes':
    print('CUDA installation directory:', cuda_dir)
    print('Host-side cuDNN installation directory:', cudnn_dir)


with open('CROSSTOOL.in', 'r') as fr:
    data = fr.read()
    data = data.replace('__TARGET_PYTHON_INCLUDES__', python_inc_dir)
    data = data.replace('__CUDA_DIR__', cuda_dir)
    with open('CROSSTOOL', 'w') as fw:
        fw.write(data)


config = configparser.ConfigParser()
config['paths'] = {
    'target_python_includes': python_inc_dir,
    'cuda_dir': cuda_dir,
    'host_cudnn_dir': cudnn_dir,
    'is_cuda': is_cuda
}

with open('.config', 'w') as f:
    config.write(f)
