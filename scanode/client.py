# Scanner for Master Node

from sys import argv

from check.hwcheck import check_cpu
from check.hwcheck import check_ram
from check.hwcheck import check_capacity
from check.hwcheck import check_ipmi_access


def _print_head():
    print '''
#===============================================================#
#                      TESTING MASTER NODE                      #
#===============================================================#
'''


def _print_foot():
    print '''
#===============================================================#
#                      FINISH TESTING                           #
#===============================================================#
'''


def run_test(test, con_info):
    '''Executes test with con_info and catches the result of it to show in
    printable view.'''

    try:
        out_str = 'Running test: "%s"' % test.__name__
        out_str = out_str + ('.'*(60 - len(out_str)))
        print out_str,

        test(con_info)

    except Exception as e:
        print 'FAIL'
        return (test.__name__, e.message)

    else:
        print 'OK'
        return (test.__name__, '')


def _print_fails(fails):
    if not fails:
        return

    print ''
    print 'Tests failed.'

    for fail in fails:
        if fail[1] == '':
            continue

        print fail[0] + ':'
        print fail[1]
        print ''


def main():

    con_info = dict()

    if len(argv) > 1:
        for arg in argv[1:]:
            if arg.startswith('--host='):
                con_info['host'] = arg[7:]
            elif arg.startswith('--user='):
                con_info['user'] = arg[7:]
            elif arg.startswith('--password='):
                con_info['password'] = arg[11:]

    _print_head()

    tests = [check_cpu, check_ram, check_capacity, check_ipmi_access]
    fails = list()

    for test in tests:
        msg = run_test(test, con_info)
        if msg != '':
            fails.append(msg)

    _print_fails(fails)
    _print_foot()

if __name__ == '__main__':
    main()
