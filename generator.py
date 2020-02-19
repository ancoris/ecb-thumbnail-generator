#!/usr/bin/env python
from __future__ import unicode_literals, print_function
import argparse
import ffmpeg
import sys
import os


parser = argparse.ArgumentParser(description='Generate video thumbnail')
parser.add_argument('input_dir', help='Directory that contains the video files')
parser.add_argument('output_dir', help='The directory of the generated thumbnails')
parser.add_argument('--time', type=int, default=420, help='Time offset')


def generate_thumbnail(in_filename, out_filename, time, dimensions):
    try:
        (
            ffmpeg
            .input(in_filename, ss=time)
            .filter('scale', dimensions)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)


def gen_thumbnails(input_dir, output_dir):
    video_directory = os.listdir(input_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for file in video_directory:
        if file.endswith("mp4") or file.endswith("mov"):
            # Generate the larger thumbnail, with a resolution of 640x360
            generate_thumbnail(os.path.join(input_dir, file),
                               os.path.join(output_dir, (os.path.splitext(file)[0]+"_1.png")),
                               args.time, "640x360")
            # Generate a small thumbnail with resolution of 120x68, with the suffix _1_n added to the filename
            generate_thumbnail(os.path.join(input_dir, file),
                               os.path.join(output_dir, (os.path.splitext(file)[0] + "_1_n.png")),
                               args.time, "120x68")


if __name__ == '__main__':
    args = parser.parse_args()
    gen_thumbnails(args.input_dir, args.output_dir)
