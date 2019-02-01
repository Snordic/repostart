#!/usr/bin/env python3.5
import sys
import os
import subprocess
import argparse

repo_ARM  = ''
repo_ATOM = ''
config_ARV = ''
config_ARR = ''
config_ATR = ''
config_ATV = ''
# print('Star work')
# subprocess.check_call(["mkdir test"], shell=True)
# print('End work')


def get_args():
    parser = argparse.ArgumentParser(description='Get UART statuses', prog=os.path.basename(__file__))
    parser.add_argument('-r', '--repo', help='Repo ARM/ATOM')
    parser.add_argument('-c', '--config', help='Сonfig Vanilla/RDKB')
    return parser.parse_args()


def repo_init(repo, repo_PATH):
    print('Start repo init')
    if (repo == 'arm'):
        if not os.path.isdir('arm'):
            os.mkdir('arm')
        os.chdir(repo_PATH + '/arm')
        subprocess.check_call(repo_ARM, shell=True)
        repo_PATH = repo_PATH + '/arm'
    elif (repo == 'atom'):
        if not os.path.isdir('atom'):
            os.mkdir('atom')
        os.chdir(repo_PATH + '/atom')
        subprocess.check_call(repo_ATOM, shell=True)
        repo_PATH = repo_PATH + '/atom'
    print('End repo init')
    print('Start repo sync')
    subprocess.check_call('repo sync -q -j4', shell=True)
    print('End repo sync')
    return repo_PATH


def source_config(repo, config, repo_PATH):
    print('Start source config')
    repo_PATH_2 = repo_PATH + '/setup'
    os.chdir(repo_PATH_2)
    if (repo == 'atom'):
        if (config == 'v'):
            genconf = config_ATV 
            repo_PATH = repo_PATH + '/atom_v/build'
        else:
            genconf = config_ATR
            repo_PATH = repo_PATH + '/atom_ros/build'
        output = subprocess.check_output(genconf, shell=True, executable="/bin/bash")
    elif (repo == 'arm'):
        output = subprocess.check_output("source arm_setup -i; env -0", shell=True, executable="/bin/bash")
        repo_PATH = repo_PATH + '/setup/build'
    print('End source config')
    return repo_PATH


def change_conf(repo_PATH):
    print('Start change conf/local.conf')
    repo_PATH = repo_PATH + '/conf/local.conf'
    with open(repo_PATH) as file_in:
        text = file_in.read()

    text = text.replace('#DL_DIR ?= "${TOPDIR}/downloads"', 'DL_DIR ?= "${TOPDIR}/downloads"')
    text = text.replace('DL_DIR ?= "${TOPDIR}/downloads"', 'DL_DIR ?= "/local/v.s/downloads"')

    text = text.replace('#DL_DIR ?= "${TOPDIR}/../downloads"', 'DL_DIR ?= "${TOPDIR}/../downloads"')
    text = text.replace('DL_DIR ?= "${TOPDIR}/../downloads"', 'DL_DIR ?= "/local/v.s/downloads"')

    text = text.replace('#SSTATE_DIR ?= "${TOPDIR}/sstate-cache"', 'SSTATE_DIR ?= "${TOPDIR}/sstate-cache"')
    text = text.replace('SSTATE_DIR ?= "${TOPDIR}/sstate-cache"', 'SSTATE_DIR ?= "/local/v.s/sstate-cache"')

    text = text.replace('#SSTATE_DIR ?= "${TOPDIR}/../sstate-cache"', 'SSTATE_DIR ?= "${TOPDIR}/../sstate-cache"')
    text = text.replace('SSTATE_DIR ?= "${TOPDIR}/../sstate-cache"', 'SSTATE_DIR ?= "/local/v.s/sstate-cache"')

    TMPDIR = 'TMPDIR = "/local/v.s/tmp/' + ((repo_PATH.split('jira/')[1]).split('/setup')[0]).split('/atom_') + '"'

    text = text.replace('#TMPDIR = "${TOPDIR}/tmp"', 'TMPDIR = "${TOPDIR}/tmp"')
    text = text.replace('TMPDIR = "${TOPDIR}/tmp"', TMPDIR)

    with open(repo_PATH, 'w') as file_out:
        file_out.write(text)
    print('End change conf/local.conf')


if __name__ == '__main__':
    args = get_args()
    repo = str(args.repo).lower()
    config = str(args.config).lower()
    repo_PATH = str(os.getcwd())
    print('What you choice: repo = {} config = {}'.format(repo, config))
    if ((repo != 'atom' and repo != 'arm') and
        (config != 'v' and config != 'r')):
        raise Exception('Error: Not chosen repo or config!')
    repo_PATH = repo_init(repo, repo_PATH)
    repo_PATH = source_config(repo, config, repo_PATH)
    change_conf(repo_PATH)
    print('end')

