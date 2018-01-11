import os


SoundLevenCmd = "amixer cset numid=6,iface=MIXER,name='Speaker Playback Volume' {}"


def ChangeSoundLevel(val):
	print('[util] Change sound level to {}'.format(val))
	os.system(SoundLevenCmd.format(val))
