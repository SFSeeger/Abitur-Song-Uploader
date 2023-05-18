# Abitur Song Uploader

A simple way to manage songs  

## Deployment on a Raspberry Pi / local PC

### Requirements

- Raspberry Pi
- Micro SD card
- Ethernet Cable (Optional)

|              | Minimum Requirements |   Recommended  |         My Hardware        |
|:------------:|:--------------------:|:--------------:|:--------------------------:|
| Raspberry Pi | Raspberry Pi 3       | Raspberry Pi 4 | Raspberry Pi 4             |
| RAM          | 2GB                  | 4GB            | 8GB                        |
| Storage      | 16GB                 | 32GB           | 64GB                       |
| Overclocked  | No                   | Yes            | 2,3GHz with active cooling |

### Raspberry Pi configuration

1. Use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to flash the micro SD card with the Ubuntu Server Image. If you use a Raspberry Pi with more than 4GB RAM use the 64bit version.
1. Create a ssh key using `ssh-keygen -t ed25519 -C "<your@email>"`
1. Connect your raspi with your network. You'll figure out how, i trust you :wink:
1. connect to your raspberry via ssh `ssh ubuntu@ubuntu`. The password should be _ubuntu_
1. create a new user called _ansible_, add it to the _sudoer_ group and set the users password

```bash
sudo useradd -m ansible
sudo usermod -aG sudo ansible
sudo passwd ansible
```

1. Run `cat ~/.ssh/id_ed25519.pub` on your machine and copy the output
1. Run `echo "<the command output> >> ~/.ssh/allowed_hosts"` and `echo "<the command output> >> /home/ansible/.ssh/allowed_hosts`
1. Run `sudo nano /etc/ssh/sshd_config.d/50-cloud-init.conf` and change `PasswordAuthentication` to _no_
1. Restart the ssh server using `sudo systemctl restart ssh`
1. Next, get a ssl certificate using [this guide](https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal) make sure to use the `certonly`

### Port forwarding

You should forward the following ports on your Router:

- 80/TCP
- 443/TCP
- 22/TCP (optional for remote ssh connection)
- 22/UDP (optional for remote ssh connection)

### Ansible configuration

Delete the `ansible/vault.yml` file and create your own. It needs to look like this:

```yml
secret_key: [random key can be made e.g. here https://miniwebtool.com/django-secret-key-generator/]
mysql_root_password: [long and strong password]
mysql_db: [database name e.g. songuploader]
mysql_user: [simple username]
mysql_password: [strong password for the user]
email_host_user: [gmail email]
email_host_password: [gmail password]
default_password: [password for gunicorn user]
admin_email: [your email]
admin_phone: [your phonenumber]
```

1. adjust your `ansible/hosts` file with your domain name
1. generate a password and save it into `ansible/.vault_pass`.
1. save your ansible user password into `ansible/.become_pass`.
1. open your command line and run the following to encrypt the vault and install the site on the raspberry

```bash
cd ansible
ansible-vault encrypt vault.yml
ansible-playbook -i hosts -u ansible --private-key=~/id_ed25519 site.yml --become-password-file .become_pass -v
```

## Create dev Environment

please create a `.env` file using the `.env.example`.
then simply run

```bash
docker compose up
```

to start server.

### Services

You have th following services at your disposal in your dev environment:

| Service    | Container Name                    | Port (service)              |
|------------|-----------------------------------|----------------------------|
| website    | abitur-song-uploader-web          | 8080 (web), 3456 (debugpy) |
| db         | abitur-song-uploader-db-1         | 3306 (mysql)               |
| pypmyadmin | abitur-song-uploader-phpmyadmin-1 | 8090 (web)                 |
| mailhog    | abitur-song-uploader-mailhog-1    | 8025 (web)                 |
