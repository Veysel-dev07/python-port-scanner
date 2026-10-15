import socket
import argparse as ap

parser = ap.ArgumentParser()
parser.add_argument('-u', '--url', required=True, help='IP or URL that you want scanned for open Ports')
parser.add_argument('-p', '--ports', nargs= '+', required=True, help='What Ports do you want to scan? (List them all, or use "-" between two numbers to go through all of the Ports in a set Range))')
parser.add_argument('-to', '--timeout', default=5.0, type=float, required=False, help='How many seconds until timeout?')
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')

args = parser.parse_args()

def scan_site():
    ports_to_scan = []
    if "-" in args.ports[0]:
        scope = args.ports[0].split("-")
        for port in range(int(scope[0]), int(scope[1]) + 1):
            ports_to_scan.append(port)
    else:
        for port in args.ports:
            ports_to_scan.append(int(port))
    ports_scan(ports_to_scan)


def service_port(port, protocol, sock):

    serviceName = socket.getservbyport(port, protocol)

    print(f"Name of the running Service : {serviceName}")
    banner = sock.recv(1024).decode().strip()
    print(f"Banner for {args.url}:{port} -> {banner}")

def ports_scan(ports):
    closed_ports = 0
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(args.timeout)
        result = s.connect_ex((args.url, port))
        if result == 0:
            print(f"Port {port} is open!")
            try:
                service_port(port, "tcp", s)       
            except socket.error as e:
                print(f"Error: {e}") 
        elif args.verbose:
            print(f"Port {port} is closed")
            closed_ports += 1
        else:
            closed_ports += 1
        s.close()
    print(f"{closed_ports} Ports are closed")

        

scan_site()

    