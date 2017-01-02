import logging
import time
import _psearch

if __name__='__main__':

    PSEARCH_VERSION = '1.0'

    logging.basicConfig(filename='pSearchLog.log', level=logging.DEBUG, format='%(asctime)s%(message)s')

    _psearch.ParseCommandLine()

    log = logging.getLogger('main._psearch')
    log.info("p-search started")

    startTime = time.time()

    _psearch.SearchWords()

    endTime = time.time()
    duration = endTime - startTime

    logging.info('Elapsed Time:' + str(duration) + 'seconds')
    logging.info('')

    logging.info('Program Terminated Normally')

