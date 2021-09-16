#!/usr/bin/env python3
from metasploit.msfrpc import MsfRpcClient
import subprocess
import os

def interactive():
    try:
        if ':55553' not in subprocess.getoutput('netstat -ntlp'):
            os.system('msfrpcd -S -a 127.0.0.1 -P test -U msf')
        while True:
            run = subprocess.getoutput('netstat -ntlp')
            if ':55553' in run: break
        rat = MsfRpcClient('test', ssl=False)
        cmd = rat.consoles.console()
        baner = cmd.read()
        baner = baner['data']
        print(baner)
        while True:
            x = cmd.read()
            console = rat.consoles.list['consoles'][-1]['prompt']
            console = console.replace('\x01\x02', '')
            run = input('\r' + console)
            if run == '':
                x = cmd.read()
                continue
            if run == 'exit': break
            cmd.write(run)
            for i in range(0, 30):
                sh = cmd.read()
                sh = sh['data']
                if sh != '':
                    print(sh)
                    sh = cmd.read()
                    break
    except KeyboardInterrupt:
        print('\rExiting program...')
        exit()
    except:
        print('\rCannot connect to msfrpc service...')

if __name__ == "__main__":
    interactive()
