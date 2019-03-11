import setuptools

with open('README.whl', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
        name = 'Pythonic',
        version = '0.6',
        author = 'Stephan Avenwedde',
        author_email = 's.avenwedde@gmail.com',
        license = 'GPLv3',
        description='A Python based trading platform for digital currencies',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/hANSIc99/Pythonic',
        packages = ['Pythonic'],
        package_dir = {'' : 'src'},
        package_data = { '' :
            ['pools.txt', 'cpu.txt', 'config.txt', 'all_mine',
                'all_mine.exe', 'libeay32.dll', 'ssleay.dll',
                'translations/*.qm', 'translations/*.png',
                'images/*.png', 'elements/*']
        },
        entry_points = {
            'console_scripts' : ['Pythonic = Pythonic.script:run']
            },
        python_requires = '>=3.5',
        install_requires = [
            'PyQt5>=5.6,<=5.8.2',
            'pandas>=0.20.3',
            'python-binance>=0.5.16'],
        classifiers = [
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Development Status :: 4 - Beta',
            'Intended Audience :: Financial and Insurance Industry',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Education',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: OS Independent',
            'Environment :: X11 Applications :: Qt',
            'Natural Language :: German',
            'Natural Language :: English',
            'Natural Language :: Chinese (Simplified)',
            'Natural Language :: Spanish',
            'Topic :: Office/Business :: Financial'
            ],
        )
