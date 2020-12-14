# Setting up a WordPress site using Nginx and PHP FPM

## Database

We will be using Mariadb instead of Mysql, as far as the end user is concerned, they behave similarly

For our use case, I will be using a different virtual machine for MySQL. I will be launching
the VM using Vagrant. This is the Vagrantfile

> Note : It does not really matter if you are using a local virtual machine or a cloud server
> like DigitalOcean or AWS. The instructions are the same

More about MySQL : 

1. Install Mariadb


```bash
sudo apt update
sudo apt install mariadb-server
```

2. Secure the installation

```bash
sudo mysql_secure_installation
```

This shall ask you a few questions. Long story short, press `Y` for all of them and follow
the instructions

3. Create the database and user for wordpress

```bash
sudo mysql
```

And in the Mariadb prompt
```
MariaDB [(none)]> CREATE DATABASE wp_site;
Query OK, 1 row affected (0.000 sec)

MariaDB [(none)]> CREATE USER 'wp_user'@'%' IDENTIFIED BY 'j7wJZmLWyebzCLZFp9qx';
Query OK, 0 rows affected (0.000 sec)

MariaDB [(none)]> GRANT ALL ON wp_site.* TO 'wp_user'@'%';
Query OK, 0 rows affected (0.000 sec)

MariaDB [(none)]> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.000 sec)
```

4. Make MariaDB listen on all network interfaces (If you are using a dedicated MariaDB server)

By default MariaDB listens only on loopback interface. But, inorder for us to reach the mariadb
from other machines, we need to make it listen on all network interfaces. You can see this using `ss`

```
vagrant@mysql-server:~$ ss -tl
State        Recv-Q        Send-Q               Local Address:Port                Peer Address:Port
LISTEN       0             80                       127.0.0.1:mysql                    0.0.0.0:*
LISTEN       0             128                        0.0.0.0:ssh                      0.0.0.0:*
LISTEN       0             128                           [::]:ssh                         [::]:*
vagrant@mysql-server:~$
```

> Note: Be careful when opening up the database server to the outside. This is usually fine
> if you are using local virtual machines, but on a cloud server, make sure you firewall your
> database server properly. Meaning, allow only those who needs to connect to the database

```
sudo vim /etc/mysql/mariadb.conf.d/50-server.cnf
```

Find the line that says `bind-address` and change it from 127.0.0.1 to 0.0.0.0

```
bind-address            = 0.0.0.0
```
And restart MariaDB
```
sudo systemctl restart mysql
```
And now we can see that mysql is listening on all interfaces
```
vagrant@mysql-server:~$ ss -tl
State        Recv-Q        Send-Q               Local Address:Port                Peer Address:Port
LISTEN       0             80                         0.0.0.0:mysql                    0.0.0.0:*
LISTEN       0             128                        0.0.0.0:ssh                      0.0.0.0:*
LISTEN       0             128                           [::]:ssh                         [::]:*
```

## PHP FPM

```
sudo apt install gnupg2

wget -q https://packages.sury.org/php/apt.gpg -O- | sudo apt-key add -
echo "deb https://packages.sury.org/php/ buster main" |sudo tee /etc/apt/sources.list.d/php.list

sudo apt update

sudo apt install php7.4-fpm php7.4-common php7.4-mysql \
php7.4-xml php7.4-xmlrpc php7.4-curl php7.4-gd \
php7.4-imagick php7.4-cli php7.4-dev  \
php7.4-mbstring php7.4-opcache  \
php7.4-soap php7.4-zip -y

```

> Note: You may not need all of these php packages, but these are the most commonly used
> Feel free to skip the ones you know you don't need


Make sure php7.4-fpm is running

```
sudo systemctl status php7.4-fpm
```


## Nginx

If you are new to Nginx, go ahead and watch this : [Configuring Nginx, VirtualHosting, /etc/hosts, Curl](https://www.youtube.com/watch?v=i6NHxKyGI7s&list=PLxYCgfC5WpnsAg5LddfjlidAHJNqRUN14&index=13)

Install Nginx
```
sudo apt install nginx -y
```

Create `/etc/nginx/sites-enabled/wordpress.devops.esc.sh`


```
server {
        listen 80;
        root /var/www/wordpress.devops.esc.sh;
        index index.php index.html index.htm index.nginx-debian.html;
        server_name wordpress.devops.esc.sh;

        location / {
                try_files $uri $uri/ /index.php$is_args$args;
        }

        location ~ \.php$ {
                include snippets/fastcgi-php.conf;
                fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
        }

        location ~ /\.ht {
                deny all;
        }
}
```


Make sure nginx works by using
```
sudo nginx -t
```

If there is any syntax error, fix it obviously

Reload Nginx
```
sudo systemctl reload nginx
```
## Updating hosts file

I will be adding an entry in my hosts file to point `wordpress.devops.esc.sh` to the IP address of the VM.
Make sure you do that. 

Add a new line with (Change where needed)
```
192.168.33.21 wordpress.devops.esc.sh
```

### Linux/Mac

In Linux/Mac, it's as simple as editing `/etc/hosts` as root

### Windows

1. Open Notepad as administrator
2. Open > c:\Windows\System32\Drivers\etc\hosts
3. Add the entry as above


## Testing if Nginx/PHP-FPM works

Before we install Wordpress, let's make sure that our nginx/php installation works as expected

```
mkdir /var/www/wordpress.devops.esc.sh
cd /var/www/wordpress.devops.esc.sh
echo '<?php phpinfo(); ?>' > info.php
```

Now open `wordpress.devops.esc.sh/info.php` and it should show the php info page. That means we
are good.

Make sure to delete the info.php file
```
rm info.php
```

## Setting up WordPress


### Download and extract

```
cd /tmp
wget https://wordpress.org/latest.tar.gz
tar xf latest.tar.gz
```

This will extract the wordpress files into a directory `wordpress`. 

Let's move it to our document root.

```
mv wordpress/* /var/www/wordpress.devops.esc.sh/
```

This means our WordPress installation is at the root of our website. So, `wordpress.devops.esc.sh` will
be loading our wordpress site. If you want it in a subdirectory, move it to it

### Configure

```
cd /var/www/wordpress.devops.esc.sh
cp wp-config-sample.php wp-config.php
```

Grab a fresh set of salts from WordPress

```
curl -s https://api.wordpress.org/secret-key/1.1/salt/
```
This will show something like

```
# curl -s https://api.wordpress.org/secret-key/1.1/salt/
define('AUTH_KEY',         'Fp:L<Ko5b7uppM-@jw+vu(V+pH !]+c)>OAOOE LB6+|DE&1tpNL[^j#jOBzQ1Y@');
define('SECURE_AUTH_KEY',  'gmCIa3334~a/-CDIj<UWleK+Z}R$;[YyyH;hgT&_%|`*]_yT(hu5y;yig-_KSAA.');
define('LOGGED_IN_KEY',    'Nu)oVM_Zx7sm!aq+=LheN}C!]Io/GMjD?tX8V%(+qr167>Cg|+|kd=HEeBa-L5gg');
define('NONCE_KEY',        '.^vF{T04>$qR_AO`B#+TF[Nbw-yLdOgTnrOwzb;yUEMDHs^U)^Ev?B8>+<e;D@8$');
define('AUTH_SALT',        'h)^r17(-[(fJm{~Bbn0tm8Sy[x.>GAZY)9-l$I4Syr2>/4SXNTsUx0F|-pDu4X?T');
define('SECURE_AUTH_SALT', 'dm{T~7JqgX&/Vz@HxO{R4<fN54R9/S.`++g6Xb^4-~3}h)- )%r+sOj+.0xM +p_');
define('LOGGED_IN_SALT',   'f[$Qg8TyQ#;b95.^+$3zZ$-RM h=LL?PRAb+(*~(h!Vy*fODrRy1}CMBTPU;PLnd');
define('NONCE_SALT',       '#B<|a vY!44q!!7PWT.bV92x~`-;>,7w{|@<%&m>ce|p|`xZ3cmxGoOb7xzrucQ/');
```

Open `wp-config.php` using your favourite editor. Use `nano` if you don't have one

```
cd /var/www/wordpress.devops.esc.sh
nano wp-config.php
```

Find the `Authentication Unique Keys and Salts.` section where there are dummy values for the above.
Replace the dummy ones with the output of the `curl -s https://api.wordpress.org/secret-key/1.1/salt/`


Now let's **update the database, user, password and the host**

In the same config file, find these and update the values accordingly

```
define( 'DB_NAME', 'wp_site' );

/** MySQL database username */
define( 'DB_USER', 'wp_user' );

/** MySQL database password */
define( 'DB_PASSWORD', 'j7wJZmLWyebzCLZFp9qx' );

/** MySQL hostname */
define( 'DB_HOST', '192.168.33.20' );
```

> Note: If you are using the same machine for Nginx, PHP and MySQL, you don't have to change `DB_HOST`


And Save and exit

(In Nano, Press `Ctrl+X` and then `Y` and enter to save the file)

### Finishing up

Now open the site in a browser

Give a title, username and password and press `Install`
This should finish the installation. You can login to the admin dashboard by visiting
`wordpress.devops.esc.sh/wp-admin`


And that is it
