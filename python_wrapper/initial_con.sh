echo "config down.."
sudo ifconfig enp0s25 down
echo "done"
echo "config set ip.."
sudo ifconfig enp0s25 192.168.123.162/24
echo "done"
echo "config up.."
sudo ifconfig enp0s25 up
echo "done"

raspberry:   ssh -l pi 192.168.123.161 - password is 123
head:        ssh -l unitree 192.168.123.13 - password is 123
side:        ssh -l unitree 192.168.123.14 - password is 123
main:        ssh -l unitree 192.168.123.15 - password is 123

