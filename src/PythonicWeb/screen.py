import os


def reset_screen():

    welcome_msg =   ' ____        _   _                 _      ____                                   \n'\
                    '|  _ \ _   _| |_| |__   ___  _ __ (_) ___|  _ \  __ _  ___ _ __ ___   ___  _ __  \n'\
                    '| |_) | | | | __| \'_ \ / _ \| \'_ \| |/ __| | | |/ _` |/ _ \ \'_ ` _ \ / _ \| \'_ \ \n'\
                    '|  __/| |_| | |_| | | | (_) | | | | | (__| |_| | (_| |  __/ | | | | | (_) | | | |\n'\
                    '|_|    \__, |\__|_| |_|\___/|_| |_|_|\___|____/ \__,_|\___|_| |_| |_|\___/|_| |_|\n'\
                    '       |___/                                                                     \n'

    version         = 'v0.18\n'
    gitHub          = 'Visit https://github.com/hANSIc99/Pythonic\n'
    log_info_msg    = '<<<<<<<<<<<< Logging directory ~/PythonicDaemon_201x/Month/\n'
    input_info_msg  = '>>>>>>>>>>>> Enter \'q\' to stop execution'
    status_info_msg = '>>>>>>>>>>>> Hold  \'p\' to list all background processes'
    applog_info_msg = '>>>>>>>>>>>> Enter \'l\' to show log messages\n'

    os.system('clear')

    print('\n')
    print(welcome_msg)
    print(version)
    print(gitHub)
    print(log_info_msg)
    print(input_info_msg)
    print(status_info_msg)
    print(applog_info_msg)