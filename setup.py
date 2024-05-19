from setuptools import setup, find_packages

setup(
    name='robotvidsub',
    version='0.1.0',
    author='Arka Mitra',
    author_email='arkamitra172@gmail.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/robotvidsub/',
    license='LICENSE.txt',
    description='Enhance Robot Framework tests by recording and subtitling videos.',
    long_description=open('README.md').read(),
    install_requires=[
        "robotframework >= 3.0",
        "ffmpeg-python",
        "ScreenCapLibrary"
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Framework :: Robot Framework",
        "Topic :: Software Development :: Testing"
    ],
    entry_points={
        'robotframework_listener': [
            'default = robotvidsub.listener:RobotVidSubListener'
        ],
    }
)
