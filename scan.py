import socket
import argparse as ap

parser = ap.ArgumentParser()
parser.add_argument('-u', '--url', help='IP or URL that you want scanned for open Ports')
parser.add_argument('-p', '--ports', nargs= '+', help='What Ports do you want to scan? (List them all, or use "-" between two numbers to go through all of the Ports in a set Range))')
parser.add_argument('-to', '--timeout', type=int, required=False, help='How many seconds until timeout?')
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')

args = parser.parse_args()

def scan_site():
    if "-" in args.ports[0]:
        scope = args.ports[0].split("-")
        anzahl_zu = 0
        for i in range(int(scope[0]), int(scope[1]) + 1):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if args.timeout is not None:
                    s.settimeout(args.timeout)
                else:
                    s.settimeout(5.0)
                result = s.connect_ex((args.url, i))
                
                if result == 0:
                    print(f"Port {i} is open!")
                    try:
                        service_port(i, "tcp")
                        banner = s.recv(1024).decode().strip()
                        print(f"Banner for {args.url}:{i} -> {banner}")       
                    except socket.error as e:
                        print(f"Error: {e}") 
                elif args.verbose:
                    print(f"Port {i} is closed")
                    anzahl_zu += 1
                else:
                    anzahl_zu += 1
                s.close()
        print(f"{anzahl_zu} Ports are closed")

    else:
        for port in args.ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5.0)
            result = s.connect_ex((args.url, int(port)))
            if result == 0:
                print(f"Port {port} is open!")
                try:
                    service_port(int(port), "tcp")
                    banner = s.recv(1024).decode().strip()
                    print(f"Banner for {args.url}:{port} -> {banner}")
                except socket.error as e:
                    print(f"Error: {e}")
            else:
                print(f"Port {port} is closed!")
        s.close()


def service_port(port, protokoll):

    serviceName = socket.getservbyport(port, protokoll)

    print(f"Name of the running Service : {serviceName}")


    

scan_site()

    