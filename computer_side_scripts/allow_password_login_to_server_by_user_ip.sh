
# allow_password_login_to_server_by_user_ip.sh
allow=$1
server_user_name=$2
server_ip=$3

ssh $server_user_name@$server_ip << EOF
    git clone https://github.com/ZPXD/tower_cybersecurity.git
    sudo python3 tower_cybersecurity/scripts/allow_server_password_login.py 0
    sudo systemctl restart ssh && sudo systemctl restart sshd
EOF



