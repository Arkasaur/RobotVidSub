# RobotVidSub

RobotVidSub is a library designed to enhance the debugging and presentation of automated tests by recording video during Robot Framework test executions and adding subtitles that display the top-level keywords in sync with the test steps shown in the video.

## Features

- **Video Recording**: Automatically starts and stops video recording, either for all tests (if a global `RECORDING` variable is set to string value `true`), or for individual tests (any test with the tag `recording` will be recorded)
- **Subtitles**: Adds subtitles to the videos, displaying the top-level keywords being executed.

## Installation

Install RobotVidSub using pip:

```
bash
pip install robotvidsub
```
## Usage

Once installed, RobotVidSub automatically integrates with your Robot Framework tests. To enable RobotVidSub on your tests, make sure the `RobotVidSub.RobotVidSubListener` listener is referenced at the time of test execution:
```
# Run tests with listener enabled - RobotVidSub.RobotVidSubListener

robot --outputdir=reports --listener=RobotVidSub.RobotVidSubListener Tests/AllTestsRun.robot
```

Ensure that the RECORDING variable is set to true in your Robot Framework environment to enable video recording of all tests. If instead you want only particular tests to be recorded, add `recording` tag to these test cases.

All recordings are stored in the `recordings` folder under your parent test folder, with the name format of `{TestCaseId}_{ExecutionStartDateTime}`

## Requirements

RobotVidSub requires the following to be installed:

* Robot Framework
* ffmpeg-python (for video processing)

These dependencies will be automatically installed when you install RobotVidSub.

Additionally, ffmpeg is needed to be installed manually on your system. You can check the installation method based on your system package manager.

Eg: For macOS with Homebrew installed, you can use
```
brew install ffmpeg
```

## Additional Notes

In order to execute the sample tests included in the Tests directory, an additional dependency   `robotframework-seleniumlibrary` needs to be installed.

The recommended installation method is using pip:

```
pip install --upgrade robotframework-seleniumlibrary
```

