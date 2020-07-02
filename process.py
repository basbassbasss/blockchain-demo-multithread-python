#!/usr/bin/env python3
import argparse
import multiprocessing
import sys
from hashlib import sha256

parser = argparse.ArgumentParser(description='Simple blockchain like mining')

parser.add_argument('message', nargs='*', help='the data')
parser.add_argument('--block', default=1, type=int, help='the block number')
parser.add_argument('--previous_hash', default='0000000000000000000000000000000000000000000000000000000000000000', help='the previous hash')
parser.add_argument('--start_nonce', default=0, type=int, help='the previous hash')
parser.add_argument('--max_nonce', default=2**32, type=int, help='the previous hash')
parser.add_argument('--difficulty', default=4, type=int, help='difficulty (e.g. leading zeros)')
parser.add_argument('--processes', default=12, type=int, help='number of processes')

args = parser.parse_args()

def get_hash(nonce, number_of_processes, max_nonce, event):
    while nonce < max_nonce:
        # Build the data
        data = str(args.block) + str(nonce) + args.message[0] + args.previous_hash
        
        # Hash the data
        hash=sha256(data.encode('utf-8')).hexdigest()

        # print(nonce)

        # See if we can find the right hash for the given difficulty
        if(hash[:args.difficulty] == '0' * args.difficulty):
            # Print the nonce and hash
            print(str(nonce) + '-' + hash)

            # Set the event for process termination
            event.set()

        nonce += number_of_processes

if __name__ == '__main__':
    processes = []

    # Create event so we can terminate all processes when a result is found
    event = multiprocessing.Event()

    # Create a range of processes based on the given start nonce and the desired amount of processes
    for i in range(args.start_nonce, args.start_nonce + args.processes):
        p = multiprocessing.Process(
            target=get_hash, 
            args=(
                i, 
                args.processes, 
                args.max_nonce,
                event
            ))

        p.start()
        processes.append(p)
    
    # Listen to the event so we can perform a termination of all processes
    while True:
        if event.is_set():
            print('Terminating processes...')
            for process in processes:
                process.terminate()
            sys.exit(1)