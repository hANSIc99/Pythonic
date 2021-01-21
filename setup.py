import setuptools

with open('README.whl', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
        name = 'Pythonic',
        version = '2.0',
        author = 'Stephan Avenwedde',
        author_email = 's.avenwedde@gmail.com',
        license = 'GPLv3',
        description='Graphical automation tool',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/hANSIc99/Pythonic',
        packages = ['Pythonic'],
        package_dir = {'' : 'src'},
        package_data = { '' :
            ['public_html/static/*.png',
             'public_html/static/qtlogo.svg',
             'public_html/static/qtloader.js',
             'public_html/static/PythonicWeb.js',
             'public_html/static/PythonicWeb.wasm',
             'public_html/templates/PythonicWeb.html',
             'public_html/config/Toolbox/*']
        },
        entry_points = {
            'console_scripts' : ['Pythonic = Pythonic.script:run']
            },
        python_requires = '>=3.7',
        install_requires = [
            'PySide2>=5.15.2',
            'eventlet>=0.27.0'],
        classifiers = [
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.7',
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
