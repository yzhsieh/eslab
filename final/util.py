import os
import re

SoundLevenCmd = "amixer cset numid=6,iface=MIXER,name='Speaker Playback Volume' {}"


def ChangeSoundLevel(val):
	print('[util] Change sound level to {}'.format(val))
	os.system(SoundLevenCmd.format(val))

def SayCreatingStream():
	print('[util] Say Creating Stream')
	os.system("mpv ./sounds/creatingstream.mp3")

def SayCrawingNews():
	print('[util] Say crawing news')
	os.system("mpv ./sounds/crawingnews.mp3")

def getint(instr):
	out = re.findall(r'\d+', instr)
	return int(out[0])


if __name__ == '__main__':
	test = "幫我播第2則新聞"
	out = re.findall(r'\d+', test)
	print(int(out[0]))