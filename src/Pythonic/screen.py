import os


def reset_screen():

    welcome_msg =   ' ____        _   _                 _      ____                                   \n'\
                    '|  _ \ _   _| |_| |__   ___  _ __ (_) ___|  _ \  __ _  ___ _ __ ___   ___  _ __  \n'\
                    '| |_) | | | | __| \'_ \ / _ \| \'_ \| |/ __| | | |/ _` |/ _ \ \'_ ` _ \ / _ \| \'_ \ \n'\
                    '|  __/| |_| | |_| | | | (_) | | | | | (__| |_| | (_| |  __/ | | | | | (_) | | | |\n'\
                    '|_|    \__, |\__|_| |_|\___/|_| |_|_|\___|____/ \__,_|\___|_| |_| |_|\___/|_| |_|\n'\
                    '       |___/                                                                     \n'

    version         = 'v1.0\n'
    gitHub          = 'Visit https://github.com/hANSIc99/Pythonic\n'
    log_info_msg    = '<<<<<<<<<<<< Logging directory ~/Pythonic/log/\n'



    os.system('clear')

    print('\n')
    print(welcome_msg)
    print(version)
    print(gitHub)
    print(log_info_msg)
    #print('working directory: {}'.format(os.getcwd()))


def reset_screen_dbg():

    input_info_msg  = '>>>>>>>>>>>> Enter \'q\' to stop execution'
    status_info_msg = '>>>>>>>>>>>> Hold  \'p\' to list all background processes handles'
    applog_info_msg = '>>>>>>>>>>>> Enter \'l\' to show log messages\n'

    print(input_info_msg)
    print(status_info_msg)
    print(applog_info_msg)