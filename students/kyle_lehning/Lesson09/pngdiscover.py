#!/usr/bin/env python3
import argparse


def parse_cmd_arguments():
    """
    Gather arguments from command line.
    """
    parser = argparse.ArgumentParser(description='List all png.')
    parser.add_argument('-i', '--input', help='input images directory', required=True)
    return parser.parse_args()


def png_search():



if __name__ == "__main__":
    ARGS = parse_cmd_arguments()