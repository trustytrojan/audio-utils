if __name__ != "__main__":
	raise BaseException("this is a script, not a module!")

import soundfile
import sounddevice
from audio_utils import util

args = util.parse_args("Speed up or slow down your audio.", {
	"input_file": {
		"help": "A file containing audio (\"-\" for stdin)"
	},

	"multiplier": {
		"type": float,
		"help": "Audio speed multiplier. If 1, the program exits."
	},

	"--codec": {
		"help": "The audio codec to encode the output file with",
		"default": "mp3",
	},

	"--output_file": {
		"help": "Where to save the new audio (\"-\" for stdout)"
	},

	"--play": {
		"help": "Play the audio instead of writing to --output_file",
		"action": "store_true"
	},

	"--dont_resample": {
		"help": "Skips the resample operation and multiplies the samplerate instead",
		"action": "store_true"
	}
})

if args.multiplier == 1:
	exit()

util.handle_stdin_stdout(args)
input_filename = util.handle_no_output_file(args)
args.output_file = f"{input_filename}-{args.multiplier}x.{args.codec}"
audio, samplerate = soundfile.read(args.input_file)

# if playing, simply change the sample rate
if args.play:
	sounddevice.play(audio, samplerate * args.multiplier, blocking=True)
	exit()

# if saving, either:
# - modify the sample rate, saving time, but losing support for MP3 (and/or other formats)
# - resample the audio, saving space, but taking some time
if args.dont_resample:
	samplerate *= args.multiplier
else:
	from scipy.signal import resample
	from numpy import size
	audio = resample(audio, int(size(audio, axis=0) * (1 / args.multiplier)))

util.save_audio(args.output_file, audio, samplerate)
