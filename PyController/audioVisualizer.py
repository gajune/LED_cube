import pyControllerMain
import struct
import math
import pyaudio
#import audioop
import numpy as np

class AudioVisualizer(pyControllerMain.PyControllerMain):
	def __init__(self, *args, **kwargs):
		super(AudioVisualizer, self).__init__(*args, **kwargs)
		self.CHUNK = 1024
		self.FORMAT = pyaudio.paInt16
		self.CHANNELS = 1
		self.RATE = 44100
		self.SAMPLE_MAX = 32767
		self.sample_size = 16
		self.pAudio = pyaudio.PyAudio()
		self.stream = self.pAudio.open(format=self.FORMAT,
					channels=self.CHANNELS,
					rate=self.RATE,
					input=True,
					frames_per_buffer=self.CHUNK)

	def update(self):
		data = self.stream.read(self.CHUNK) #
		#rms = audioop.rms(data, 2)
		#print (rms)
		indata = np.array(struct.unpack('%dh'%self.CHUNK,data))
		fft = np.absolute(np.fft.rfft(indata, n=len(indata)))
		freq = np.fft.fftfreq(len(fft), d=1./self.RATE)
		max_freq = abs(freq[fft == np.amax(fft)][0]) / 2
		max_amplitude = np.amax(indata)

		bars = np.zeros(8)

		step = int(len(fft) / len(bars))
		for i in range(len(bars)):
			bars[i] = np.mean(fft[i:i+step])

		self.clearAllPixel()

		for i, bar in enumerate(bars):
			height = min(300 * bar / float(self.SAMPLE_MAX), 8)
			for amp in range(0, int(height)):
				for y in range(0, 8):
					self.setPixelOn(i, y, amp)

if __name__ == '__main__':
	audio = AudioVisualizer()
	audio.setup()
	audio.mainLoop()
