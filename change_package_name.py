#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess

import click


def rename_package_name(old_name, new_name, verbose=False):
    """ Replaces the passed package name (old_name)
        with the new package name (new_name) recursively in all files
    """

    script_name = os.path.basename(__file__)
    # ! Terminal:
    # * $ grep --exclude=script_name -lr old | xargs sed -i 's/old/new/g'
    grep = subprocess.Popen(
        [
            'grep',
            '--exclude={}'.format(script_name),
            '--exclude-dir=.git',
            '-lr', str(old_name)
        ],
        stdout=subprocess.PIPE)

    xargs_sed = subprocess.Popen(
        [
            'xargs',
            'sed',
            '-i',
            's/{0}/{1}/g'.format(old_name, new_name)
        ],
        stdin=grep.stdout, stdout=subprocess.PIPE)

    # ! check result:
    xargs_sed.wait()
    if xargs_sed.returncode == 0:
        if verbose:
            click.secho('[!] Next files have been modified:', fg='yellow')
            subprocess.run(['grep', '--exclude-dir=.git', '-lr', new_name])
        message = '[+] Replacement completed successfully: {0} for {1}'.format(
            old_name, new_name)
        click.secho(message, fg='green')
    else:
        message = '[-] Error, try again! Check old or new package name.'
        click.secho(message, fg='red')


def rename_package_dir_name(old_name, new_name):
    """ Replaces the name of the package directory (old_name)
        with the new name of the package directory (new_name)
    """

    ls = subprocess.Popen(['ls'], stdout=subprocess.PIPE)
    grep = subprocess.Popen(
        ['grep', old_name],
        stdin=ls.stdout,
        stdout=subprocess.PIPE,
        encoding='utf-8').stdout.readline().rstrip()
    # ! check result:
    if not grep or grep == new_name:
        click.secho('[-] Error! the directory has not been renamed!', fg='red')
        click.secho('[!] Check old or new package name.', fg='yellow')
    else:
        # * Terminal: $ mv old_name/ new_name
        subprocess.run(['mv', grep + '/', new_name])


def clean_cache():
    """
    Remove all __pycache__ folders and .pyc / .pyo files from python3 project.
    ! Terminal command:
    * $ find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf # noqa W605
    This will remove all *.pyc files and __pycache__ directories recursively
    in the current directory.
    """

    find = subprocess.Popen(['find', '.'], stdout=subprocess.PIPE)
    grep = subprocess.Popen(
        ['grep', '-E', '(__pycache__|\.pyc|\.pyo$)'],  # noqa W605
        stdin=find.stdout, stdout=subprocess.PIPE)
    xargs_rm = subprocess.Popen(['xargs', 'rm', '-rf'], stdin=grep.stdout)
    # ! check result:
    xargs_rm.wait()
    if xargs_rm.returncode == 0:
        message = '[+] Cache clean!'
        click.secho(message, fg='green')
    else:
        message = '[-] Error! Cache not clean. Maybe you have already cleaned.'
        click.secho(message, fg='red')


@click.command()
@click.option('--find', '-f', help='package name to rename', required=True)
@click.option('--rename', '-r', help='new package name', required=True)
@click.option('--clean', '-c', help='clean cache files', is_flag=True)
@click.option('--verbose', '-v', help='show modified files', is_flag=True)
def start(find, rename, clean, verbose):
    """
    This decorated function runs a script.
    TODO: setup script
    ! Terminal:
    * $ python3 script_name.py -f old_name -r new_name -c -v
    """
    if clean:
        clean_cache()
    rename_package_name(find, rename, verbose)
    rename_package_dir_name(find, rename)


if __name__ == "__main__":
    start()
