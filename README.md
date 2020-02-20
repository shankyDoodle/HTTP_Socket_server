# HTTP Server 
A small HTTP sever is created using socket programming in python.
Multiple client requests are handled using multi threading. 

### How To run server:
* Open terminal at project directory and then run following command.


    $ python3 server.py

* Server will be up and running on port number [8081]


### How to test Server:

Hit following URL either by wget command or on any browser

    http://{hostAddress}:8081/{fileName}
    
Where, hostAddress = IP address of a system where server is running, &
       fileName = Name of file which we want to access.
    E.g.
    
    http://127.0.0.1:8081/hello.html