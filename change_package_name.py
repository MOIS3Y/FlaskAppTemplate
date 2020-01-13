#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import optparse
import subprocess


def get_arguments():
    """ Get's command line arguments entered by user """

    parser = optparse.OptionParser()
    parser.add_option(
        '-f', '--find', dest='find', help='package name to rename')
    parser.add_option(
        '-r', '--rename', dest='rename', help='new package name')
    (options, arguments) = parser.parse_args()
    if not options.find:
        parser.error(
            '[-] Please enter a package name, use --help for more info')
    elif not options.rename:
        parser.error(
            '[-] Please enter a package name, use --help for more info')
    return options


def rename_package_name(old_name, new_name):
    """ Replaces the passed package name (old_name)
        with the new package name (new_name) recursively in all files """

    script_name = os.path.basename(__file__)
    # * Terminal:
    # * $ grep --exclude=script_name -lr old | xargs sed -i 's/old/new/g'
    grep = subprocess.Popen(
        ['grep', '--exclude={}'.format(script_name), '-lr', str(old_name)],
        stdout=subprocess.PIPE)
    xargs_sed = subprocess.Popen(
        ['xargs', 'sed', '-i', 's/{0}/{1}/g'.format(old_name, new_name)],
        stdin=grep.stdout,
        stdout=subprocess.PIPE)
    xargs_sed.wait()
    # ! check result:
    if xargs_sed.returncode == 0:
        message = '[+] Replacement completed successfully: {0} for {1}'.format(
            old_name, new_name)
        subprocess.run(
            ['grep', '--exclude={}'.format(script_name), '-lr', new_name])
    else:
        message = '[-] Error, try again! Check old or new package name.'
    print(message)


def rename_package_dir_name(old_name, new_name):
    """ Replaces the name of the package directory (old_name)
        with the new name of the package directory (new_name) """

    ls = subprocess.Popen(['ls'], stdout=subprocess.PIPE)
    grep = subprocess.Popen(
        ['grep', old_name],
        stdin=ls.stdout,
        stdout=subprocess.PIPE,
        encoding='utf-8').stdout.readline().rstrip()
    # ! check result:
    if not grep or grep == new_name:
        print('[-] Error! the directory has not been renamed!')
        print('[!] Check old or new package name.')
    else:
        # * Terminal: $ mv old_name/ new_name
        subprocess.run(['mv', grep + '/', new_name])


# TODO: setup script: Terminal $python3 script_name.py -f old_name -r new_name
if __name__ == "__main__":
    options = get_arguments()
    rename_package_name(options.find, options.rename)
    rename_package_dir_name(options.find, options.rename)
