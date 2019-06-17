#!/usr/bin/python3

from sys import argv
from country import build


def __argument_fetcher__():
    args = {}
    if(argv[1] == 'build'):
        args = {'args': ['build']}
    return args


def __show_usage__():
    print('[+]Usage ::\n\n\tBuild Country Info : ./{} build\n'.format(argv[0]))
    return


def app():
    if(len(argv) != 2):
        __show_usage__()
        return
    args = __argument_fetcher__().get('args', [])
    if(args and args[0] == 'build'):
        result = build()
        if(result.get('success', 'false') == 'true'):
            print('[+]Success !!!')
        else:
            print('[!]Error : {}'.format(result.get('error', ':/')))
    else:
        __show_usage__()
    return


if __name__ == '__main__':
    try:
        app()
    except KeyboardInterrupt:
        print('\n[!]Terminated !!!')
    finally:
        exit(0)
