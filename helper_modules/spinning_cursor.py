import itertools, sys, time

'''
    Terminal spinning cursor simulator
'''
def spinning_cursor(time_to_wait):
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    for _ in range(time_to_wait):
        sys.stdout.write(spinner.next())
        sys.stdout.flush()
        time.sleep(1)
        sys.stdout.write('\b')