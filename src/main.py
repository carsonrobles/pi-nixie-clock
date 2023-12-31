from datetime import datetime
import logging
import time

import gpiozero as gpio


def get_log_file_name():
    LOG_PATH = '/etc'
    date_str = datetime.now().strftime("%y%m%d_%H%M%S")
    return f'{LOG_PATH}/nixie_clock_{date_str}.log'


def init_logging(log_fn):
    logging.basicConfig(format='[%(asctime)s] %(levelname)-8s %(message)s',
                        level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S',
                        filename=log_fn, encoding='utf-8')
    logging.debug(f'initialized logging to file {log_fn}')


def get_nixie_time():
    return datetime.now().strftime("%H%M")


def main():
    init_logging(get_log_file_name())
    logging.info('starting nixie clock')

    written_time = ''
    while True:
        nixie_time = get_nixie_time()
        if nixie_time != written_time:
            logging.info(f'setting clock time to {nixie_time}')
            written_time = nixie_time

        time.sleep(1)


if __name__ == '__main__':
    main()
