# allow_password_login_to_server.sh
allow=$1
server_name=$2

ssh $server_name << EOF
    git clone https://github.com/ZPXD/tower_cybersecurity.git
    sudo python3 tower_cybersecurity/scripts/allow_server_password_login.py $allow
    sudo systemctl restart ssh && sudo systemctl restart sshd
EOF


