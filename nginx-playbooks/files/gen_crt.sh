#生成自签证书
openssl req -x509 -nodes  -sha256 -days 3650 -newkey rsa:2048 -subj /CN=hello.zq.com -keyout nginx.key -out nginx.crt
