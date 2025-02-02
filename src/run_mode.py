
import argparse

def make_parser(modes):
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers()
  for mode in modes:
    mode(subparsers)
  return parser

def parse_args(parser, argv=None):
  args = parser.parse_args(argv)
  if hasattr(args, 'func'):
    return args
  else:
    parser.print_help()
    exit(0)

def run(modes, argv=None):
  parser = make_parser(modes)
  args = parse_args(parser, argv)
  return args.func(args)
