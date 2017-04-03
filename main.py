import socket 
import re 
import os 
import urllib.parse

HOST, PORT = '', 8888 

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
listen_socket.bind((HOST, PORT)) 
listen_socket.listen(1) 


def send_answer(conn, status="200 OK", typ="text/plain; charset=utf-8", data=""):
	data = data.encode("utf-8")
	conn.send(b"HTTP/1.1 " + status.encode("utf-8") + b"\r\n")
	conn.send(b"Server: simplehttp\r\n")
	conn.send(b"Connection: close\r\n")
	conn.send(b"Content-Type: " + typ.encode("utf-8") + b"\r\n")
	conn.send(b"Content-Length: " + bytes(len(data)) + b"\r\n")
	conn.send(b"\r\n")
	conn.send(data)

def page(dir_name, dir_list, conn, addr) :
	#Власне скрипт
	
	if 'index.html' in dir_list :
		file = open("index.html", "r", encoding = "utf-8")
		answer = file.read()

		send_answer(conn, typ="text/html; charset=utf-8", data=answer)
	
	
	else :
		if dir_name[-1] != '/':
			dir_name += '/'	
	
		answer = """<!DOCTYPE html>"""
		answer += """<html><head><title>задача</title></head><body>""" 

		for directs in dir_list :
			if os.path.isdir(dir_name+directs): 
				path =  dir_name + directs
				path = urllib.parse.unquote(path, encoding = "utf-8")
				print (path)
				answer += "<p><a href="+'"' + path + '">' + directs  + "</a></p>"
			else:
				answer += "<p>" + directs + "</p>"

		answer += """</body></html>"""

		send_answer(conn, typ="text/html; charset=utf-8", data=answer)


while True: 
	client_connection, client_address = listen_socket.accept() 
	request = client_connection.recv(1024) 
	res = re.findall('GET ([\w/]+) HTTP', str(request)) 


	http_response = b''
	 
	if len(res) != 0: 
		res = res[0] 
		res = urllib.parse.quote(res)
		print (res)

		list_dir = os.listdir(path="C:{}".format(res))
		
		try:
			page(res, list_dir, client_connection, client_address)
		except:
			send_answer(client_connection, "500 Internal Server Error", data="Ошибка")
		finally:
			client_connection.close()

		

