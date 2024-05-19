from datetime import datetime
from functools import reduce
from robot.libraries.BuiltIn import BuiltIn
import re
import math
import os
import ffmpeg

class RobotVidSubListener():
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        """
        Initializes the listener with default values.
        """
        self._kw_level = 0
        self._filename = ""
        self.kw_list = []
        self.segment_list = [0]
        self.start_time = datetime.now()
        self.recording_flag = BuiltIn().get_variable_value('${RECORDING}').lower()

    def start_test(self, name, attrs):
        """
        Called when a test starts. Handles the initiation of video recording.
        """
        self._filename = attrs['originalname'] + "_" + datetime.now().strftime("%Y%m%d_%H_%M_%S")
        recording = self.recording_flag if self.recording_flag == 'true' else ('true' if 'recording' in attrs['tags'] else 'false')
        if recording == 'true':
            BuiltIn().import_library("ScreenCapLibrary")
            BuiltIn().run_keyword_and_ignore_error("Start Video Recording", f"name={self._filename}")

    def end_test(self, name, attrs):
        """
        Called when a test ends. Handles the stopping of video recording and the generation of subtitled videos.
        """
        recording = self.recording_flag if self.recording_flag == 'true' else ('true' if 'recording' in attrs['tags'] else 'false')
        if recording == 'true':
            BuiltIn().import_library("ScreenCapLibrary")
            BuiltIn().run_keyword_and_ignore_error("Stop Video Recording")
        print("Subtitled video will be available at:" + self.add_subtitle_to_video(self.generate_subtitle_file()))
        # cleanup
        path = os.getcwd() + '/reports'
        os.remove(f"{path}/{self._filename}_1.webm")
        os.remove(f"{path}/{self._filename}.srt")
        self._filename = ""

    def start_keyword(self, name, attrs):
        """
        Called at the start of each keyword. Filters out 'Set Variable' keywords and processes others.
        """
        self._kw_level += 1
        if self._kw_level == 1 and attrs['kwname'] != 'Set Variable':
            parsed_kw = self.generate_parsed_kw(attrs['kwname'], attrs['args'])
            print(parsed_kw)
            self.kw_list.append(parsed_kw)

    def end_keyword(self, name, attrs):
        """
        Called at the end of each keyword. Calculates elapsed time and updates segments for subtitles.
        """
        self._kw_level -= 1
        if self._kw_level == 0 and attrs['kwname'] != 'Set Variable':
            print(f"Elapsed Time: {attrs['elapsedtime']}")
            curr_elapsed_time = datetime.now() - self.start_time
            print(f"New Elapsed Time: {int((curr_elapsed_time.total_seconds())*1000)}")
            self.segment_list.append(int((curr_elapsed_time.total_seconds())*1000))

    def generate_parsed_kw(self, kw_name, kw_args=[]):
        """
        Parses keywords to replace variables with their actual values.
        """
        parsed_kw_name = kw_name
        parsed_kw_args = ''
        kw_name_arg_list = re.findall('\${.*?}', kw_name)
        for i in kw_name_arg_list:
            parsed_kw_name = parsed_kw_name.replace(i, BuiltIn().get_variable_value(i))
        for i in kw_args:
            parsed_kw_args += "    " + BuiltIn().get_variable_value(i)
        return parsed_kw_name + parsed_kw_args

    def generate_subtitle_file(self):
        """
        Generates a subtitle file based on the keywords and their timings.
        """
        path = os.getcwd() + '/reports'
        subtitle_file = f"{path}/{self._filename}.srt"
        text = ""
        for index, segment in enumerate(self.kw_list):
            segment_start = self.format_time(self.segment_list[index])
            segment_end = self.format_time(self.segment_list[index+1])
            text += f"{str(index+1)}\n{segment_start} --> {segment_end}\n{self.kw_list[index]}\n\n"
        with open(subtitle_file, "w") as f:
            f.write(text)
        return subtitle_file

    def add_subtitle_to_video(self, subtitle_file):
        """
        Adds subtitles to the recorded video.
        """
        path = os.getcwd() + '/reports'
        input_video = f"{path}/{self._filename}_1.webm"
        video_input_stream = ffmpeg.input(input_video)
        output_video = input_video.replace(".webm", ".mp4")
        stream = ffmpeg.output(video_input_stream, output_video, vf=f"subtitles={subtitle_file}")
        ffmpeg.run(stream, overwrite_output=True)
        return output_video

    def format_time(self, milliseconds):
        """
        Formats milliseconds into a time string suitable for subtitles.
        """
        hours = math.floor(milliseconds / 3600000)
        minutes = math.floor((milliseconds % 3600000) / 60000)
        seconds = math.floor((milliseconds % 60000) / 1000)
        milliseconds = milliseconds % 1000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"