# 🧪 Practical 4 — FTP File Transfer between Windows and Ubuntu VM

## 🎯 Objective

To set up an FTP server on an Ubuntu Virtual Machine and transfer files between the host (Windows 11) and the guest (Ubuntu VM).

---

## 📋 Prerequisites

- VirtualBox or VMware installed
- Ubuntu VM with sudo access
- Windows 11 host machine
- Network connectivity between host and VM

---

## 🪜 Step-by-Step Procedure

### **Step 1: Start the Ubuntu Virtual Machine**

1. Open **VirtualBox** (or VMware)
2. Start your **Ubuntu VM**
3. Wait for the system to fully boot

---

### **Step 2: Open Terminal and Switch to Root**

Open the terminal in Ubuntu and run:

```bash
sudo su
```

> 💡 **Note:** Enter your Ubuntu password when prompted.

---

### **Step 3: Update Packages and Install FTP Server**

Update the package list and install vsftpd (Very Secure FTP Daemon):

```bash
apt update && apt install vsftpd -y
```

⏳ Wait for the installation to complete.

---

### **Step 4: Backup the Default Configuration File**

Create a backup of the original configuration file:

```bash
cp /etc/vsftpd.conf /etc/vsftpd.conf.backup
```

> 🔒 This allows you to restore the original configuration if needed.

---

### **Step 5: Edit the FTP Configuration File**

Open the configuration file in a text editor:

```bash
sudo gedit /etc/vsftpd.conf
```

**Delete all existing content**, then paste the following configuration:

```bash
# Example config file for vsftpd server
# ===============================
# BASIC CONFIGURATION
# ===============================
listen=YES
listen_ipv6=NO
local_enable=YES
write_enable=YES
local_umask=022
anonymous_enable=NO
chroot_local_user=YES
user_sub_token=$USER
local_root=/home/$USER/ftp

# ===============================
# LOGGING & MESSAGES
# ===============================
xferlog_enable=YES
dirmessage_enable=YES
use_localtime=YES
ftpd_banner=Welcome to your FTP Server on Ubuntu!

# ===============================
# CONNECTION SETTINGS
# ===============================
connect_from_port_20=YES
pasv_enable=YES
pasv_min_port=40000
pasv_max_port=50000

# ===============================
# SECURITY SETTINGS
# ===============================
secure_chroot_dir=/var/run/vsftpd/empty
pam_service_name=vsftpd
ssl_enable=NO
utf8_filesystem=YES
allow_writeable_chroot=YES
```

**Save and close** the file (`Ctrl + S`, then close gedit).

---

### **Step 6: Create FTP Directory Structure**

Replace `<user>` with your actual Ubuntu username (e.g., `om`):

```bash
mkdir -p /home/<user>/ftp/files
sudo chown -R <user>:<user> /home/<user>/ftp
sudo chmod a-w /home/<user>/ftp
sudo chmod 755 /home/<user>/ftp/files
```

**Example for username "om":**
```bash
mkdir -p /home/om/ftp/files
sudo chown -R om:om /home/om/ftp
sudo chmod a-w /home/om/ftp
sudo chmod 755 /home/om/ftp/files
```

> 📁 This creates a secure directory structure for FTP file transfers.

---

### **Step 7: Restart the FTP Service**

Apply the configuration changes by restarting the service:

```bash
sudo systemctl restart vsftpd
```

Verify the service is running:

```bash
sudo systemctl status vsftpd
```

---

### **Step 8: Check Your IP Address**

Find your Ubuntu VM's IP address:

```bash
ip a
```

Look for an IP address like `192.168.x.x` or `10.0.x.x` under interfaces like `eth0`, `enp0s3`, or `ens33`.

> 📝 **Note down this IP address** — you'll need it for the Windows connection.

**Example output:**
```
inet 192.168.153.128/24
```

---

### **Step 9: Connect from Windows**

1. Open **Command Prompt** (`cmd`) or **PowerShell** on Windows
2. Navigate to a directory where you want to transfer files from
3. Connect to the FTP server:

```cmd
ftp 192.168.153.128
```

> Replace `192.168.153.128` with your actual Ubuntu VM IP address.

4. When prompted, enter:
   - **Username:** Your Ubuntu username
   - **Password:** Your Ubuntu password

**Successful login message:**
```
230 Login successful.
ftp>
```

---

### **Step 10: Transfer a File**

Create a test file on Windows (if you don't have one):

```cmd
echo This is a test file > sample.txt
```

Upload the file to Ubuntu:

```ftp
put sample.txt
```

✅ **Success message:**
```
226 Transfer complete.
```

---

### **Step 11: Verify Transfer**

#### On Windows (in FTP session):

List files in the FTP directory:

```ftp
ls
```

You should see `sample.txt` listed.

#### On Ubuntu (in terminal):

View the uploaded file:

```bash
cat /home/<user>/ftp/files/sample.txt
```

> 🎉 If you see the file contents, the transfer was successful!

---

### **Step 12: Close FTP Connection**

Exit the FTP session:

```ftp
bye
```

or

```ftp
quit
```

---

## 📚 Common FTP Commands Reference

| Command | Description |
|---------|-------------|
| `ls` | List files in the current directory |
| `cd <directory>` | Change directory |
| `pwd` | Print working directory |
| `put <filename>` | Upload file from local to remote |
| `get <filename>` | Download file from remote to local |
| `mput <pattern>` | Upload multiple files |
| `mget <pattern>` | Download multiple files |
| `delete <filename>` | Delete file on server |
| `bye` / `quit` | Close FTP connection |
| `help` | Show available commands |

---

## 🔧 Troubleshooting

### Connection refused
- Check if vsftpd service is running: `sudo systemctl status vsftpd`
- Verify firewall settings: `sudo ufw status`
- Allow FTP through firewall: `sudo ufw allow 20:21/tcp`

### Login failed
- Verify username and password are correct
- Check user exists: `cat /etc/passwd | grep <username>`
- Ensure `local_enable=YES` in config file

### Cannot upload files (550 Permission denied)
- Check directory permissions
- Verify `write_enable=YES` in config
- Ensure user owns the upload directory

### Passive mode issues
- Ensure ports 40000-50000 are open in firewall
- Check network mode in VM settings (use Bridged or NAT with port forwarding)

---

## ✅ Conclusion

You have successfully:
- ✓ Installed and configured an FTP server on Ubuntu
- ✓ Connected from Windows to Ubuntu via FTP
- ✓ Transferred files between the two systems

This setup can be used for file sharing in local network environments.

---

## 🔐 Security Notes

> ⚠️ **Warning:** This configuration uses unencrypted FTP. For production environments, consider:
> - Using SFTP (SSH File Transfer Protocol) instead
> - Enabling SSL/TLS (FTPS) by setting `ssl_enable=YES`
> - Restricting FTP access to specific users
> - Using strong passwords

---

**Last Updated:** October 2025  
**Tested On:** Ubuntu 22.04/24.04 LTS with Windows 11