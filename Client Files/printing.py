import subprocess

def print_it(receipt_txt=b'Hello There'):
    try:
        data = open('Order_file.txt', 'rb').read()
    except:
        pass
    lpr =  subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
    lpr.stdin.write(data)



print_it()