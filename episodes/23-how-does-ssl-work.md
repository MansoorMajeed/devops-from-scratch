# How does SSL (TLS) work

Video Link [HERE](https://youtu.be/pc5Xf9uuvwE)

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

HTTPS = HTTP + SSL

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

## What does TLS do for us

1. Makes sure that the data we are sending/receiving is only seen by us and the server - Encryption
2. Ensures that the server we are talking to is the right one - Authentication
3. Makes sure that no one tampers with the data. That is, if you sent "Hello" to your friend in Facebook
messenger, they should receive exactly the same. No one should be able to tamper with it over the network - Integrity

## TLS Terminology

Before we talk about how TLS works, it is important to take a look at the terms we use when we talk about TLS


### Encryption

You know this one. This is the process of converting a human readable plain text into a non human-readable format.
Just like the above example

Encryption makes sure that, only us and the server can read the data, no one else on the network can.

### Types of Encryption

There are mainly two types of Encryption

#### Symmetric Encryption

In this, both parties uses the same key to encrypt and decrypt the data. Example: AES

But the problem is that, both parties need to know the shared key to be able to encrypt or
decrypt. So, this is a challenge when dealing with communications across a network.

#### Asymmetric Encryption (Public key encryption)

There is a key pair. They are called public and private key. For example, using `ssh-keygen` we have generated SSH
key pair. They are always related to each other.

If you encrypt something with one key, you can decrypt it only using the other key.

So, if I encrypt something using the public key, only the private key associated with it can decrypt it.

### Ciphers

Algorithms used to encrypt/decrypt data

### TLS Certificate

A text file with a bunch of information like the owner of a domain, expiry of the certificate, who approved this certificate
the public key etc. This is sent by the server to the client.

This is how it looks like being used in a webserver configuration
```
ssl_certificate /etc/letsencrypt/live/ssl.demo.esc.sh/fullchain.pem;
```

The certificate itself looks like this

```
head /etc/letsencrypt/live/ssl.demo.esc.sh/fullchain.pem                                                                                                                                                                    root@hydrogen
-----BEGIN CERTIFICATE-----
MIIFazCCBFOgAwIBAgISBKNEQbcYxhnjsYe613NE1rsvMA0GCSqGSIb3DQEBCwUA
MEoxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MSMwIQYDVQQD
ExpMZXQncyBFbmNyeXB0IEF1dGhvcml0eSBYMzAeFw0yMDA5MjcwNTI0MDVaFw0y
MDEyMjYwNTI0MDVaMBoxGDAWBgNVBAMTD3NzbC5kZW1vLmVzYy5zaDCCASIwDQYJ
KoZIhvcNAQEBBQADggEPADCCAQoCggEBALvT6DX2U9C8i0iVmDGEicq2H4Gk56Ee
ROPbOWuz+7kSxHXAOHFGffrKpsKvPfpx+pq8V56PwZQZz/mbEEFjd2lRDrIZi0nR
SLoYL3pQVptkyfCGQAzAfBvZQqonZ0AgPcJZ4CjIQCn9w/S4SOuKzSOlhyX+2Jzo
G3BIA8Jtvfs4UkL17Z+nT8SbUeDmykbNp1CvlqS9EVYaoMUevt9frV5oV0MzsNSA
8/4ZO9nzoztptpgf1H2NH30ZTBMoZAdVbDKAh4Un+Urwlc9XZagv9HaCw5tpyEpa
```

You can fetch a domain's certificate using the command

```
openssl s_client -showcerts -connect ssl.demo.esc.sh:443 -servername ssl.demo.esc.sh </dev/null 2>/dev/null
```

You can also get the certificate information by looking at your browser.
Click on the padlock -> Certificate. It looks like this

![SSL Cert info](img/ssl-info.png)

> TLS Certificates are public, not secret (unlike the private key)

### Who issues these certificates - Certificate Authority (CA)

To be able to have the browser trust a website's TLS certificate, this needs to be issued by
one of the Certificate Authorities

So if you own a domain, say `esc.sh` and you want to make your website secure using TLS, you can
approach a certificate authority and ask for a certificate. They will ask you to prove that you own
the domain. Once you have proved it, they will give you the certificate (Hugely oversimplified)

In the old days you had to pay for these certificates, but now you can get one for free from
Let's Encrypt.

#### What is special about CAs

The certificate authorities are trusted by all the browsers. So, if the browser sees that the
server it is connecting to have a certificate that is issued by a known CA in its list, then it will trust
it (provided the expiry is with in the tiomeframe and other information are correct)

### Private key

The other half of the public key encryption. It can decrypt whatever is encrypted using the public key.
Also, it can encrypt stuff that can be decrypted using the public key


It looks like this in Nginx configuration
```
ssl_certificate_key /etc/letsencrypt/live/ssl.demo.esc.sh/privkey.pem;
```

And the file itself looks like this
> Do not post your private key anywhere. I edited it out and replaced it with the
> certificate itself ;) So, good luck with trying to guess the private key ;)

```
head /etc/letsencrypt/live/ssl.demo.esc.sh/privkey.pem
-----BEGIN PRIVATE KEY-----
MIIFazCCBFOgAwIBAgISBKNEQbcYxhnjsYe613NE1rsvMA0GCSqGSIb3DQEBCwUA
MEoxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MSMwIQYDVQQD
ExpMZXQncyBFbmNyeXB0IEF1dGhvcml0eSBYMzAeFw0yMDA5MjcwNTI0MDVaFw0y
MDEyMjYwNTI0MDVaMBoxGDAWBgNVBAMTD3NzbC5kZW1vLmVzYy5zaDCCASIwDQYJ
KoZIhvcNAQEBBQADggEPADCCAQoCggEBALvT6DX2U9C8i0iVmDGEicq2H4Gk56Ee
ROPbOWuz+7kSxHXAOHFGffrKpsKvPfpx+pq8V56PwZQZz/mbEEFjd2lRDrIZi0nR
SLoYL3pQVptkyfCGQAzAfBvZQqonZ0AgPcJZ4CjIQCn9w/S4SOuKzSOlhyX+2Jzo
G3BIA8Jtvfs4UkL17Z+nT8SbUeDmykbNp1CvlqS9EVYaoMUevt9frV5oV0MzsNSA
8/4ZO9nzoztptpgf1H2NH30ZTBMoZAdVbDKAh4Un+Urwlc9XZagv9HaCw5tpyEpa
```
### Can I make my own ceritificates?

Yes, they are called self signed certificates. Since they are not trusted by a CA, your browser won't
trust that certificate. But you can add your own CA and trust it in your browser. This way, all certificates
issued by your own CA will work on your browsers (Remember, this means it will only work on browsers where
you have installed your own CA certificates)

## How does TLS encryption works - TLS Handshakes

The process that encrypts the communication between a client and a server is called **TLS (SSL) Handshake**

When a user visits a website with TLS enabled, this is what happens

1. **Client Hello** (Plain) : The handshake is initiated by the client. This hello message includes:
    - Tthe versions of TLS/SSL the client supports
    - The cipher suite it supports
    - "client random" - a random string
2. **Server Hello** (Plain) : The server replies with the following
    - Chosen cipher suite
    - Server's TLS certificate
    - "server random" - another random string
3. **Authentication** (Plain) : The client
    - Looks at the certificate the server sent, looks at the CA, expiry etc
    - If it matches the domain name, not expired, trusted CA then it validates the authenticity of the website
    - Remember that the client also got the public key of the server from the certificate
4. **Premaster secret** (Key is encrypted with public key): The client
    - Generates another random string
    - Encrypts it using the server's public key (Now, only the server can decrypt it)
    - Sends it to the server
5. **Premaster secret decrypted** : The server uses its private key to decrypt the premaster secret
6. **Session keys created**: Both the client and the server generates the session key using
    - Client random + Server random + premaster secret = Session key
    - Both the server and the client will have the same key (symmetric)
7. **Client Ready** (Symmetric encrypted) : Client sends ready message which is encrypted using the session key
8. **Server ready** (Symmetric encrypted) : Server sends ready message which is encrypted using the same session key
9. **Encrypted channel created** : Going from here, until a new session is created, everything is encrypted. This includes your
credit card details, usernames, passwords, the URL etc


![How SSL Works](img/how-ssl-works.png)
