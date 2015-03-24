# Scanner for Master Node

from sys import argv

from check.hwcheck import CHECKS


def _print_head(host):

    len_row = 79

    caption = 'TESTING NODE '
    lspace = (len_row - len(caption) - len(host) - 2) / 2
    rspace = len_row - lspace - len(caption) - len(host) - 2

    print '#%s#' % ('='*(len_row-2))
    print '#%s%s%s%s#' % (' ' * lspace,
                          caption,
                          host,
                          ' ' * rspace
                          )
    print '#%s#' % ('='*(len_row-2))
    print ''


def _print_sep_traceback():

    len_row = 79
    print '\n#%s#\n' % ('=' * (len_row - 2))


def _print_foot():

    len_row = 79

    caption = 'FINISH TESTING'

    lspace = (len_row - len(caption) - 2) / 2
    rspace = len_row - lspace - len(caption) - 2

    print '#%s#' % ('='*(len_row-2))
    print '#%s%s%s#' % (' ' * lspace,
                        caption,
                        ' ' * rspace
                        )
    print '#%s#' % ('='*(len_row-2))
    print ''


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
        return ()


def _print_fails(fails):

    if not fails:
        print '\n\[ TEST PASSED ]\n'
        return

    print '\n[ TEST FAILED ]\n'

    for fail in fails:
        print '> {test_name}:\n{err_msg}\n'.format(test_name=fail[0],
                                                   err_msg=fail[1])


def main():

    con_info = {}

    if len(argv) > 1:
        for arg in argv[1:]:
            if arg.startswith('--host='):
                con_info['host'] = arg[7:]
            elif arg.startswith('--user='):
                con_info['user'] = arg[7:]
            elif arg.startswith('--password='):
                con_info['password'] = arg[11:]

    if 'host' not in con_info.keys():
        raise KeyError('Host is not specified.')

    _print_head(con_info['host'])

    fails = []

    for test in CHECKS:
        test_result = run_test(test, con_info)

        if test_result:
            fails.append(test_result)

    _print_sep_traceback()
    _print_fails(fails)
    _print_foot()

if __name__ == '__main__':
    main()
