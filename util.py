from argparse import Namespace
from tempfile import NamedTemporaryFile
from sys import stdin, stdout
from soundfile import write
from typing import Any
from argparse import ArgumentParser

def parse_args(arguments: dict[str, Any], program_desc: str):
	arg_parser = ArgumentParser(description=program_desc)
	for key, value in arguments.items():
		arg_parser.add_argument(key, **value)
	return arg_parser.parse_args()

def handle_stdin_stdout(args: Namespace):
	# save the audio from stdin into a tmpfile; soundfile does not like raw buffers
	if args.input_file == "-":
		temp_file = NamedTemporaryFile(delete=False)
		temp_file.write(stdin.buffer.read())
		temp_file.close()
		args.input_file = temp_file.name

	if args.output_file == "-":
		args.output_file = stdout.buffer

def handle_no_output_file(args: Namespace):
	if args.output_file is not None:
		return
	def highest_index(target: str) -> int:
		for i in range(len(args.input_file) - 1, -1, -1):
			if args.input_file[i] == target:
				return i
		return -1
	input_filename = args.input_file[highest_index("/") + 1 : highest_index(".")]
	args.output_file = f"{input_filename}-{args.multiplier}x.{args.codec}"

def save_audio(args: Namespace, audio, samplerate: int):
	# save the modified audio (or samplerate)
	if args.output_file is stdout.buffer:
		# again soundfile doesn't like raw buffers, we must specify the format
		# i could make more arguments for this but for now we will force the use of WAV
		write(args.output_file, audio, samplerate, format="WAV", subtype="PCM_32", endian="CPU")
	else:
		write(args.output_file, audio, samplerate)
