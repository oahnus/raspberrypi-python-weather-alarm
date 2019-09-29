#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pyaudio
import wave
import os
import logging
import time

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.StreamHandler()],
    format='%(levelname)s:%(asctime)s:%(message)s'
)

class VoicePlayer:

    def __init__(self) -> None:
        self.chunk = 1024

    def _is_wav(self, f):
        res = True
        try:
            wave.open(f)
        except wave.Error as e:
            res = False
        return res

    def _pcm2wav(self, pcm_file, save_file, channels=1, bits=16, sample_rate=16000):
        """ pcm转换为wav格式
            Args:
                pcm_file pcm文件
                save_file 保存文件
                channels 通道数
                bits 量化位数，即每个采样点占用的比特数
                sample_rate 采样频率
        """
        if self._is_wav(pcm_file):
            raise ValueError('"' + str(pcm_file) + '"' +
                             " is a wav file, not pcm file! ")

        pcmf = open(pcm_file, 'rb')
        pcmdata = pcmf.read()
        pcmf.close()

        if bits % 8 != 0:
            raise ValueError("bits % 8 must == 0. now bits:" + str(bits))

        wavfile = wave.open(save_file, 'wb')

        wavfile.setnchannels(channels)
        wavfile.setsampwidth(bits // 8)
        wavfile.setframerate(sample_rate)

        wavfile.writeframes(pcmdata)
        wavfile.close()


    def play(self, filename='voice.wav'):
        if (filename.endswith(".pcm")):
            self._pcm2wav('voice.pcm', 'voice.wav')
            filename = 'voice.wav'

        logging.debug("[VoicePlayer.play] - load file %s" % filename)
        chunk = 1024
        wf = wave.open(filename, 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True)
        data = wf.readframes(chunk)

        while data != '':
            stream.write(data)
            data = wf.readframes(chunk)
            if data == b'':
                break

        stream.close()
        p.terminate()
        logging.debug("[VoicePlayer.play] - Voice Play Finish")

if __name__ == '__main__':
    player = VoicePlayer()
    player.play()
