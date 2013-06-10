from distutils.core import setup

setup(
	name='django-sape',
	description='Django + sape.ru.',
	version='0.2.4',
	packages=\
	[
		'sape',
		'sape.management',
		'sape.management.commands',
		'sape.templatetags',
	],
	author='Dimmma',
	author_email='https://github.com/Dimmma',
	maintainer='Mikhail Fedosov',
	maintainer_email='tbs.micle@gmail.com',
	url='http://github.com/fedosov/sape',
	keywords=['Django', 'sape', 'sape.ru', ],
	#install_requires=['mechanize']
	classifiers=
	[
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: Python Software Foundation License',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: POSIX',
		'Programming Language :: Python',
	],
)
