# How does SSL (TLS) work

## What is SSL/TLS

- `SSL` stands for Secure Sockets Layer. 
- `TLS` Stands for Transport Layer Security

These are protocols designed to provide security for communications between devices
in a network. Long story short, these protocols helps in making sure that the sensitive
information we send over a network is not captured by a third party (like a hacker)

For example, when you access your bank's website and login with your username and passsword
these information are being transferred over the network from your computer all the way to the
servers of the bank. SSL/TLS makes sure that only your bank's server can actually see what
you are sending them

## SSL vs TLS vs HTTPS

### HTTPS

This is the odd one among the three. HTTPS stands for Hypertext Transfer Protocol Secure. This
is the secure version of the HTTP protocol, which is used to transfer data between computers.
For example, when you open a website like google.com, your browser and google.com's servers use
`http` and the server sends the webpage to your browser.

HTTPS = HTTPS + SSL

### TLS vs SSL

TLS is the newer version of SSL. It goes like this

SSLv2.0 -> SSLv3.0 -> TLSv1.0 -> TLSv1.1 -> TLSv1.2 -> TLSv1.3

> SSLv1 was never released publicly

So, long story short, after 3.0, SSL was renamed to TLS. So, going forward, it is better to use
the term TLS.


## What is wrong with HTTP?

If you are in a coffee shop and you are connecting to a website over `http` and not `https`, someone
running some software looking at the packets in the network can see everything you are doing. Including
your username and password. Now, this is obviously terrible. The reason this happens is because the
protocol `http` sends everything in plain text.

But, with TLS, in https, everything you send is encrypted. So, even though someone snooping in the network
will be able to see that you are sending something, they will not able to read it as it would look like garbage
to them

For example, if I make an http request with a username and password, like this

```
curl 'http://login.demo.esc.sh/index.php' --data-raw 'user_id=admin&user_pass=secret'
```
Someone looking at the packets would be able to see this:

```
0..../..POST /index.php HTTP/1.1
Host: login.demo.esc.sh
User-Agent: curl/7.64.1
Accept: */*
Content-Length: 30
Content-Type: application/x-www-form-urlencoded

user_id=admin&user_pass=secret
```

That is, our username and password. 

However, if I send the same request over https
```
curl 'https://login.demo.esc.sh/index.php' --data-raw 'user_id=admin&user_pass=secret'
```

This is all they can see.

```
.......b.#....E..8.N@.6....;*	........JF...X.o....d1.....
.1@.0..........6.*..4....m\.J.O.....j......|...T..^3.>.....G.......K.......m#..].....7..r,..E.	m.2./o...\..0h.K.=..e.v._..R.l9.p?`Q.B...,..".)p<....`......ZHP}..v./..:.....U <...J.Y@,A.F..>=mH..W.e.J.{.|Y...I..c]
.=.f(Y..x...!.H.M|....]O.T..
\.a..{......*..u..I..	5.K.
```

I know which version I prefer for the shady hacker to see 
