import socket
import ssl
import datetime
from domain_helper import domain, domainencoder
import jsonpickle

HOST, PORT = "localhost", 9999
domains_url = [
"",
"",
]


def ssl_expiry_datetime(hostname):
    ssl_dateformat = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    context.check_hostname = False

    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    # 5 second timeout
    conn.settimeout(5.0)

    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    # Python datetime object
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_dateformat)


if __name__ == "__main__":
    for value in domains_url:
        now = datetime.datetime.now()
        try:
            expire = ssl_expiry_datetime(value)
            diff = expire - now
            #print("Domain name: {} Expiry Date: {} Expiry Day: {}".format(value,expire.strftime("%Y-%m-%d"),diff.days))
            dom = domain(value, expire.strftime("%Y-%m-%d") ,diff.days)
            domjson = jsonpickle.encode(dom, unpicklable=False)
            print(domjson)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                # Connect to server and send data
                sock.connect((HOST, PORT))
                sock.sendall(domjson)

                # Receive data from the server and shut down
                received = sock.recv(1024)
            finally:
                sock.close()

            print("Sent{}".format(domjson))
            print("Received: {}".format(received))
        except Exception as e:
            print(e)
