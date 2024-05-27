from setuptools import setup, find_packages

setup(
    name='RobotVidSub',
    version='0.1.0',
    author='Arka Mitra',
    author_email='arkamitra172@gmail.com',
    packages=find_packages(),
    url='https://github.com/Arkasaur/RobotVidSub',
    license='LICENSE.txt',
    description='Enhance Robot Framework tests by recording and subtitling videos.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "robotframework >= 3.0",
        "ffmpeg-python",
        "robotframework-screencaplibrary"
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Framework :: Robot Framework",
        "Topic :: Software Development :: Testing",
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'robotframework_listener': [
            'default = robotvidsub.listener:RobotVidSubListener'
        ],
    }
)
