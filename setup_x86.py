import setuptools

with open('README.whl', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
        version = '1.11',
        author = 'Stephan Avenwedde',
        author_email = 's.avenwedde@gmail.com',
        license = 'GPLv3',
        description='Graphical automation tool',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/hANSIc99/Pythonic',
        packages = ['Pythonic', 'Pythonic.executables'],
        package_dir = { '' : 'src'},
        package_data = { '' :
            [
             'public_html/static/ManualScheduler.png',
             'public_html/static/Scheduler.png',
             'public_html/static/ManualStopProcess.png',
             'public_html/static/StopProcess.png',
             'public_html/static/GenericPipe.png',
             'public_html/static/GenericProcess.png',
             'public_html/static/ProcessPipe.png',
             'public_html/static/Telegram.png',
             'public_html/static/Email.png',
             'public_html/static/CCXT.png',
             'public_html/static/CCXT_Method.png',
             'public_html/static/SQLite.png',
             'public_html/static/python.ico',
             'public_html/static/qtlogo.svg',
             'public_html/static/qtloader.js',
             'public_html/static/*.js',
             'public_html/static/*.wasm',
             'public_html/static/*.data',
             'public_html/templates/*.html',
             'public_html/config/Toolbox/0Basic/*',
             'public_html/config/Toolbox/1IO/2SQLite.json',
             'public_html/config/Toolbox/1IO/SQLite.editor',
             'public_html/config/Toolbox/2Connectivity/Telegram.editor',
             'public_html/config/Toolbox/2Connectivity/0Telegram.json',
             'public_html/config/Toolbox/2Connectivity/EMail.editor',
             'public_html/config/Toolbox/2Connectivity/1EMail.json',
             'public_html/config/Toolbox/3Trading/*'
             ]
        },
        entry_points = {
            'console_scripts' : ['Pythonic = Pythonic.script:run']
            },
        python_requires = '>=3.7',
        classifiers = [
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Development Status :: 4 - Beta',
            'Intended Audience :: Manufacturing',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: OS Independent',
            'Environment :: Web Environment',
            'Environment :: Console',
            'Natural Language :: English',
            'Topic :: Software Development'
            ],
        )
