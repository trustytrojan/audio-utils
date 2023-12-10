if __name__ != "__main__":
	raise BaseException("this is a script, not a module!")

import soundfile
import sounddevice
import util

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

	"--codec": {
		"help": "The audio codec to encode the output file with",
		"default": "mp3",
	},

	"--output_file": {
		"help": 'Where to save the audio slice ("-" for stdout)'
	},

	"--play": {
		"help": "Play the audio instead of writing to --output_file",
		"action": "store_true"
	}
})

util.handle_stdin_stdout(args)
util.handle_no_output_file(args)

def hms_to_sec(time_str: str):
	time_split = tuple(map(int, time_str.split(":")))
	match len(time_split):
		case 3:
			hours, minutes, seconds = time_split
			return 3600 * hours + 60 * minutes + seconds
		case 2:
			minutes, seconds = time_split
			return 60 * minutes + seconds
		case 1:
			return time_split[0]
	raise ValueError("time_str not in hh:mm:ss or lesser format")

start_time_sec = hms_to_sec(args.start_time)
end_time_sec = hms_to_sec(args.end_time)

audio, samplerate = soundfile.read(args.input_file)

# get a slice of the audio from start_time to end_time
audio = audio[start_time_sec * samplerate : end_time_sec * samplerate]

if args.play:
	sounddevice.play(audio, samplerate, blocking=True)
	exit()

util.save_audio(args, audio, samplerate)
