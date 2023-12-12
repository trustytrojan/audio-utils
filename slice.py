if __name__ != "__main__":
	raise BaseException("this is a script, not a module!")

import soundfile
import sounddevice
from audio_utils import util

args = util.parse_args("Cut a slice of audio.", {
	"input_file": {
		"help": 'A file containing audio ("-" for stdin)'
	},

	"start_time": {
		"help": "Start time in seconds, or in hh:mm:ss format"
	},

	"end_time": {
		"help": "End time in seconds, or in hh:mm:ss format"
	},

	"--save": {
		"help": 'Where to save the audio slice ("-" for stdout)'
	},

	"--codec": {
		"help": "The audio codec to encode the output file with",
		"default": "mp3",
	},

	"--play": {
		"help": "Play the audio instead of writing to --output_file",
		"action": "store_true"
	}
})

args.output_file = args.save # for compatibility
util.handle_stdin_stdout(args)
args.save = args.output_file

audio, samplerate = soundfile.read(args.input_file)

def hms_to_sample(time_str: str):
	time_split = tuple(map(float, time_str.split(":")))
	match len(time_split):
		case 3:
			hours, minutes, seconds = time_split
			return int((3600 * hours + 60 * minutes + seconds) * samplerate)
		case 2:
			minutes, seconds = time_split
			return int((60 * minutes + seconds) * samplerate)
		case 1:
			return int(time_split[0] * samplerate)
	raise ValueError("time_str not in hh:mm:ss or lesser format")

start_sample = 0 if args.start_time == "-" else hms_to_sample(args.start_time)
end_sample = (len(audio) - 1) if args.end_time == "-" else hms_to_sample(args.end_time)

# get a slice of the audio from start_time to end_time
audio = audio[start_sample : end_sample]

if args.play:
	sounddevice.play(audio, samplerate, blocking=True)
	exit()

util.save_audio(args.save, audio, samplerate)
