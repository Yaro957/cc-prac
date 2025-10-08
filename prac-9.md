# 🧪 Practical No. 9 — Implement and Use Security Features of OpenStack Cloud

## Complete Step-by-Step Guide

---

## **Aim**

To implement basic security features of an OpenStack-based private cloud using MicroStack, including security groups (firewall rules) and key pairs (SSH authentication).

---

## **Prerequisites**

Before starting this practical, ensure you have:
- ✅ Completed Practical No. 8 (OpenStack MicroStack Installation)
- ✅ MicroStack running and accessible
- ✅ Access to Horizon dashboard
- ✅ OpenStack CLI functional
- ✅ At least one VM instance running (or ability to create one)

---

## **System Requirements**

| Component | Requirement |
|-----------|-------------|
| **Installed Cloud** | OpenStack (MicroStack) from Practical 8 |
| **Instance** | Cirros or Ubuntu VM |
| **Internet** | Required for package downloads and testing |
| **Access** | Horizon dashboard or CLI |
| **OS** | Ubuntu 20.04/22.04 (host machine) |
| **Terminal** | SSH client installed |

---

## **Theory**

### What is Cloud Security?

**Cloud Security** encompasses the technologies, policies, and controls deployed to protect data, applications, and infrastructure in cloud computing environments.

**Key Security Aspects:**
- **Authentication:** Verifying user identity
- **Authorization:** Controlling resource access
- **Encryption:** Protecting data in transit and at rest
- **Network Security:** Controlling traffic flow
- **Access Control:** Managing who can access what

### OpenStack Security Components

#### 1. **Security Groups**

Security groups act as **virtual firewalls** that control inbound and outbound traffic to instances.

**Features:**
- Rule-based access control
- Stateful firewall (return traffic automatically allowed)
- Applied to instances at launch or afterward
- Multiple security groups can be assigned to one instance

**Default Behavior:**
- All outbound traffic is allowed
- All inbound traffic is denied (unless explicitly allowed)

#### 2. **Key Pairs**

Key pairs provide **secure SSH authentication** using public-key cryptography.

**Components:**
- **Private Key:** Kept secret on your local machine
- **Public Key:** Stored in OpenStack and injected into instances

**Advantages over passwords:**
- More secure (2048-4096 bit encryption)
- Cannot be brute-forced
- No password transmission over network
- Can be revoked without changing passwords

#### 3. **Other Security Features**

- **Keystone:** Identity and access management
- **Network isolation:** Virtual networks and subnets
- **Volume encryption:** Encrypted block storage
- **API security:** Token-based authentication

---

## **Complete Procedure**

### **Part A: Working with Security Groups**

Security groups control network access to your instances using firewall rules.

---

#### **Step 1: Understanding Default Security Group**

##### 1.1 List Existing Security Groups (CLI)

```bash
microstack.openstack security group list
```

**Expected output:**
```
+--------------------------------------+---------+------------------------+
| ID                                   | Name    | Description            |
+--------------------------------------+---------+------------------------+
| xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | default | Default security group |
+--------------------------------------+---------+------------------------+
```

##### 1.2 View Default Security Group Rules

```bash
microstack.openstack security group rule list default
```

**Expected output:**
```
+--------------------------------------+-------------+-----------+-----------+
| ID                                   | IP Protocol | IP Range  | Port Range|
+--------------------------------------+-------------+-----------+-----------+
| xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | None        | 0.0.0.0/0 | -         |
| xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | None        | ::/0      | -         |
+--------------------------------------+-------------+-----------+-----------+
```

**Default rules allow:**
- All outbound traffic
- All traffic from same security group

**Default rules block:**
- All inbound traffic from external sources

##### 1.3 View via Horizon Dashboard

1. Log in to Horizon dashboard (`http://localhost`)
2. Navigate to **Project → Network → Security Groups**
3. Click on **default** security group
4. Go to **Manage Rules** tab
5. Review existing rules

---

#### **Step 2: Create Custom Security Group**

##### 2.1 Create Security Group (CLI)

```bash
microstack.openstack security group create \
  --description "Security group for web server" \
  web-server-sg
```

**Expected output:**
```
+-------------+--------------------------------------+
| Field       | Value                                |
+-------------+--------------------------------------+
| id          | xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx |
| name        | web-server-sg                        |
| description | Security group for web server        |
+-------------+--------------------------------------+
```

##### 2.2 Create Security Group (Horizon)

1. Go to **Project → Network → Security Groups**
2. Click **+ Create Security Group**
3. Fill in details:
   - **Name:** `web-server-sg`
   - **Description:** `Security group for web server`
4. Click **Create Security Group**

---

#### **Step 3: Add Security Group Rules**

##### 3.1 Allow SSH Access (Port 22) - CLI

```bash
microstack.openstack security group rule create \
  --protocol tcp \
  --dst-port 22 \
  --remote-ip 0.0.0.0/0 \
  web-server-sg
```

**Explanation:**
- `--protocol tcp`: Use TCP protocol
- `--dst-port 22`: SSH port
- `--remote-ip 0.0.0.0/0`: Allow from any IP (use specific IP for production)
- `web-server-sg`: Target security group

**Expected output:**
```
+-------------------+--------------------------------------+
| Field             | Value                                |
+-------------------+--------------------------------------+
| direction         | ingress                              |
| ethertype         | IPv4                                 |
| id                | xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx |
| port_range_max    | 22                                   |
| port_range_min    | 22                                   |
| protocol          | tcp                                  |
| remote_ip_prefix  | 0.0.0.0/0                            |
| security_group_id | xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx |
+-------------------+--------------------------------------+
```

##### 3.2 Allow HTTP Access (Port 80) - CLI

```bash
microstack.openstack security group rule create \
  --protocol tcp \
  --dst-port 80 \
  --remote-ip 0.0.0.0/0 \
  web-server-sg
```

##### 3.3 Allow HTTPS Access (Port 443) - CLI

```bash
microstack.openstack security group rule create \
  --protocol tcp \
  --dst-port 443 \
  --remote-ip 0.0.0.0/0 \
  web-server-sg
```

##### 3.4 Allow ICMP (Ping) - CLI

```bash
microstack.openstack security group rule create \
  --protocol icmp \
  --remote-ip 0.0.0.0/0 \
  web-server-sg
```

##### 3.5 Allow Custom Port Range - CLI

Example: Allow ports 8000-8100:

```bash
microstack.openstack security group rule create \
  --protocol tcp \
  --dst-port 8000:8100 \
  --remote-ip 0.0.0.0/0 \
  web-server-sg
```

##### 3.6 Add Rules via Horizon Dashboard

1. Go to **Project → Network → Security Groups**
2. Click on **web-server-sg**
3. Click **Manage Rules**
4. Click **+ Add Rule**

**For SSH Rule:**
- **Rule:** `SSH`
- **Remote:** `CIDR`
- **CIDR:** `0.0.0.0/0` (or specific IP)
- Click **Add**

**For HTTP Rule:**
- **Rule:** `HTTP`
- **Remote:** `CIDR`
- **CIDR:** `0.0.0.0/0`
- Click **Add**

**For Custom Rule:**
- **Rule:** `Custom TCP Rule`
- **Direction:** `Ingress`
- **Port:** `8080` (or range `8000-8100`)
- **Remote:** `CIDR`
- **CIDR:** `0.0.0.0/0`
- Click **Add**

##### 3.7 Verify Security Group Rules

```bash
microstack.openstack security group rule list web-server-sg
```

**Expected output:**
```
+--------------------------------------+-------------+-----------+------------+
| ID                                   | IP Protocol | Port Range| IP Range   |
+--------------------------------------+-------------+-----------+------------+
| xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | tcp         | 22:22     | 0.0.0.0/0  |
| xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | tcp         | 80:80     | 0.0.0.0/0  |
| xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | tcp         | 443:443   | 0.0.0.0/0  |
| xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | icmp        | -         | 0.0.0.0/0  |
+--------------------------------------+-------------+-----------+------------+
```

---

#### **Step 4: Apply Security Group to Instance**

##### 4.1 Add Security Group to Existing Instance (CLI)

```bash
microstack.openstack server add security group <instance-name> web-server-sg
```

Example:
```bash
microstack.openstack server add security group test-vm web-server-sg
```

##### 4.2 Remove Security Group from Instance (CLI)

```bash
microstack.openstack server remove security group <instance-name> web-server-sg
```

##### 4.3 Launch New Instance with Security Group

```bash
microstack.openstack server create \
  --image cirros \
  --flavor m1.small \
  --network test \
  --security-group web-server-sg \
  --security-group default \
  secure-vm
```

##### 4.4 Apply Security Group via Horizon

**For existing instance:**
1. Go to **Project → Compute → Instances**
2. Click dropdown arrow next to instance
3. Select **Edit Security Groups**
4. Move `web-server-sg` to **Instance Security Groups**
5. Click **Save**

**For new instance:**
1. During instance creation (Step 6: Security Groups)
2. Select required security groups
3. Proceed with launch

---

#### **Step 5: Test Security Group Rules**

##### 5.1 Get Instance IP Address

```bash
microstack.openstack server show secure-vm -f value -c addresses
```

Example output: `test=10.20.20.45`

##### 5.2 Test ICMP (Ping)

From host machine:

```bash
ping 10.20.20.45
```

**Expected result:** Should receive replies if ICMP rule is added.

##### 5.3 Test SSH Access

```bash
ssh cirros@10.20.20.45
```

**Note:** You'll need the key pair (covered in Part B) for successful SSH login.

##### 5.4 Test HTTP Access (if web server running)

```bash
curl http://10.20.20.45
```

Or open in browser: `http://10.20.20.45`

---

#### **Step 6: Security Group Best Practices**

##### 6.1 Principle of Least Privilege

**❌ Bad practice:**
```bash
# Allow all traffic from anywhere
--remote-ip 0.0.0.0/0 --dst-port 1:65535
```

**✅ Good practice:**
```bash
# Allow only specific port from specific IP
--remote-ip 192.168.1.100/32 --dst-port 22
```

##### 6.2 Use Specific IP Ranges

Instead of `0.0.0.0/0`, use:
- Your office IP: `203.0.113.50/32`
- Your network: `192.168.1.0/24`
- VPN subnet: `10.8.0.0/24`

##### 6.3 Separate Security Groups by Purpose

Create different security groups for different roles:
- `web-server-sg`: Ports 80, 443
- `database-sg`: Port 3306 (only from web servers)
- `admin-sg`: Port 22 (only from admin IPs)

---

### **Part B: Working with Key Pairs**

Key pairs provide secure SSH authentication without passwords.

---

#### **Step 7: Understanding Key Pairs**

Key pairs consist of:
1. **Private Key (.pem file):** Stored on your local machine (keep secure!)
2. **Public Key:** Stored in OpenStack and injected into instances

**Authentication Flow:**
1. User attempts SSH connection
2. Server sends challenge encrypted with public key
3. Client decrypts with private key
4. If successful, access granted

---

#### **Step 8: Create Key Pair**

##### 8.1 Create Key Pair (CLI Method)

```bash
microstack.openstack keypair create --private-key ~/mykey.pem mykey
```

**Expected output:**
```
+-------------+-------------------------------------------------+
| Field       | Value                                           |
+-------------+-------------------------------------------------+
| fingerprint | xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx |
| name        | mykey                                           |
| user_id     | xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx            |
+-------------+-------------------------------------------------+
```

This creates:
- Private key saved to `~/mykey.pem`
- Public key stored in OpenStack

##### 8.2 Set Correct Permissions

```bash
chmod 400 ~/mykey.pem
```

**Why 400?**
- Owner can read only
- No one else has any permissions
- SSH requires private keys to be protected

##### 8.3 Verify Key Pair Creation

```bash
microstack.openstack keypair list
```

**Expected output:**
```
+--------+-------------------------------------------------+
| Name   | Fingerprint                                     |
+--------+-------------------------------------------------+
| mykey  | xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx |
+--------+-------------------------------------------------+
```

##### 8.4 View Key Pair Details

```bash
microstack.openstack keypair show mykey
```

---

#### **Step 9: Create Key Pair via Horizon Dashboard**

##### 9.1 Navigate to Key Pairs

1. Log in to Horizon dashboard
2. Go to **Project → Compute → Key Pairs**
3. Click **+ Create Key Pair**

##### 9.2 Create New Key Pair

**Method 1: Generate New Key**
1. **Key Pair Name:** `mykey-horizon`
2. **Key Type:** `SSH Key`
3. Click **Create Key Pair**
4. Browser will download `mykey-horizon.pem`
5. Save it securely

**Method 2: Import Existing Public Key**
1. Click **Import Public Key**
2. **Key Pair Name:** `imported-key`
3. **Key Type:** `SSH Key`
4. **Public Key:** Paste your existing public key
5. Click **Import Key Pair**

##### 9.3 Secure Downloaded Key

```bash
# Move to secure location
mv ~/Downloads/mykey-horizon.pem ~/.ssh/

# Set permissions
chmod 400 ~/.ssh/mykey-horizon.pem
```

---

#### **Step 10: Use Existing SSH Key**

##### 10.1 Generate SSH Key Pair Locally

If you don't have an SSH key:

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/openstack-key
```

**Prompts:**
- Enter passphrase (optional but recommended)
- Confirm passphrase

**Generated files:**
- Private key: `~/.ssh/openstack-key`
- Public key: `~/.ssh/openstack-key.pub`

##### 10.2 Import Public Key to OpenStack

```bash
microstack.openstack keypair create \
  --public-key ~/.ssh/openstack-key.pub \
  openstack-key
```

##### 10.3 Verify Import

```bash
microstack.openstack keypair list
```

---

#### **Step 11: Launch Instance with Key Pair**

##### 11.1 Launch Instance (CLI)

```bash
microstack.openstack server create \
  --image cirros \
  --flavor m1.small \
  --network test \
  --key-name mykey \
  --security-group web-server-sg \
  secure-vm-with-key
```

**Note:** `--key-name mykey` injects the public key into the instance.

##### 11.2 Launch Instance (Horizon)

1. Go to **Project → Compute → Instances**
2. Click **Launch Instance**

**Instance Details:**
- **Instance Name:** `secure-vm-web`
- Follow steps for Source, Flavor, Networks

**Key Pair Tab:**
- **Available Key Pairs:** Select `mykey` or `mykey-horizon`
- Click the **+** to add it

**Security Groups Tab:**
- Select `web-server-sg` and `default`

3. Click **Launch Instance**

##### 11.3 Verify Instance Launch

```bash
microstack.openstack server list
```

Wait for Status: `ACTIVE`

---

#### **Step 12: SSH into Instance Using Key Pair**

##### 12.1 Get Instance IP Address

```bash
microstack.openstack server show secure-vm-with-key -f value -c addresses
```

Example output: `test=10.20.20.50`

##### 12.2 SSH Using Private Key

```bash
ssh -i ~/mykey.pem cirros@10.20.20.50
```

**For Ubuntu instances:**
```bash
ssh -i ~/mykey.pem ubuntu@10.20.20.50
```

**Expected output:**
```
The authenticity of host '10.20.20.50' can't be established.
ECDSA key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.20.20.50' (ECDSA) to the list of known hosts.
$ 
```

You're now logged in!

##### 12.3 Troubleshooting SSH Connection

**Problem: Permission denied (publickey)**

```bash
# Verify key permissions
ls -l ~/mykey.pem
# Should show: -r-------- (400)

# If not, fix it:
chmod 400 ~/mykey.pem
```

**Problem: Connection timeout**

```bash
# Check security group allows SSH
microstack.openstack security group rule list web-server-sg | grep 22

# Check instance has floating IP (if needed)
microstack.openstack server show secure-vm-with-key
```

**Problem: Wrong username**

Try different usernames:
- Cirros: `cirros`
- Ubuntu: `ubuntu`
- CentOS: `centos`
- Debian: `debian`

---

#### **Step 13: Key Pair Management**

##### 13.1 List All Key Pairs

```bash
microstack.openstack keypair list
```

##### 13.2 Show Key Pair Details

```bash
microstack.openstack keypair show mykey
```

##### 13.3 Delete Key Pair

```bash
microstack.openstack keypair delete mykey
```

**⚠️ Warning:** This only deletes the public key from OpenStack. Your private key file remains on your local machine.

##### 13.4 Delete Key Pair via Horizon

1. Go to **Project → Compute → Key Pairs**
2. Select checkbox next to key pair
3. Click **Delete Key Pairs**
4. Confirm deletion

---

### **Part C: Combined Security Implementation**

#### **Step 14: Create Secure Web Server Instance**

##### 14.1 Preparation

Let's create a complete secure instance with:
- Custom security group (SSH + HTTP + ICMP)
- SSH key pair authentication
- Ubuntu image for web server

##### 14.2 Create Security Group

```bash
microstack.openstack security group create \
  --description "Secure web server security group" \
  secure-webserver-sg
```

##### 14.3 Add Security Rules

```bash
# Allow SSH from specific IP (replace with your IP)
microstack.openstack security group rule create \
  --protocol tcp \
  --dst-port 22 \
  --remote-ip 192.168.1.0/24 \
  secure-webserver-sg

# Allow HTTP from anywhere
microstack.openstack security group rule create \
  --protocol tcp \
  --dst-port 80 \
  --remote-ip 0.0.0.0/0 \
  secure-webserver-sg

# Allow HTTPS from anywhere
microstack.openstack security group rule create \
  --protocol tcp \
  --dst-port 443 \
  --remote-ip 0.0.0.0/0 \
  secure-webserver-sg

# Allow ICMP for monitoring
microstack.openstack security group rule create \
  --protocol icmp \
  --remote-ip 0.0.0.0/0 \
  secure-webserver-sg
```

##### 14.4 Create/Verify Key Pair

```bash
# If you haven't created one yet
microstack.openstack keypair create --private-key ~/.ssh/webserver-key.pem webserver-key
chmod 400 ~/.ssh/webserver-key.pem
```

##### 14.5 Launch Secure Instance

```bash
microstack.openstack server create \
  --image cirros \
  --flavor m1.small \
  --network test \
  --key-name webserver-key \
  --security-group secure-webserver-sg \
  my-secure-webserver
```

##### 14.6 Verify and Access

```bash
# Check status
microstack.openstack server list

# Get IP address
microstack.openstack server show my-secure-webserver -f value -c addresses

# SSH into instance
ssh -i ~/.ssh/webserver-key.pem cirros@<instance-ip>
```

---

#### **Step 15: Install and Test Web Server (Optional)**

If using Ubuntu image instead of Cirros:

##### 15.1 SSH into Instance

```bash
ssh -i ~/.ssh/webserver-key.pem ubuntu@<instance-ip>
```

##### 15.2 Update System

```bash
sudo apt update
sudo apt upgrade -y
```

##### 15.3 Install Apache Web Server

```bash
sudo apt install apache2 -y
```

##### 15.4 Start Apache

```bash
sudo systemctl start apache2
sudo systemctl enable apache2
```

##### 15.5 Create Test Page

```bash
echo "<h1>Secure OpenStack Web Server</h1>" | sudo tee /var/www/html/index.html
```

##### 15.6 Test from Host Machine

```bash
curl http://<instance-ip>
```

Or open in browser: `http://<instance-ip>`

**Expected output:**
```html
<h1>Secure OpenStack Web Server</h1>
```

---

### **Part D: Security Monitoring and Auditing**

#### **Step 16: Monitor Security Events**

##### 16.1 View Instance Console Log

```bash
microstack.openstack console log show my-secure-webserver
```

This shows boot messages and login attempts.

##### 16.2 Check Failed SSH Attempts (from instance)

```bash
# SSH into instance
ssh -i ~/.ssh/webserver-key.pem ubuntu@<instance-ip>

# View authentication logs
sudo grep "Failed password" /var/log/auth.log
sudo grep "authentication failure" /var/log/auth.log
```

##### 16.3 List Active Security Groups

```bash
microstack.openstack security group list
```

##### 16.4 Audit Security Group Rules

```bash
# Check all rules for a security group
microstack.openstack security group rule list secure-webserver-sg --long
```

---

#### **Step 17: Security Best Practices Implementation**

##### 17.1 Restrict SSH Access by IP

Instead of allowing SSH from anywhere (`0.0.0.0/0`), use specific IPs:

```bash
# Delete existing SSH rule (if any)
microstack.openstack security group rule list secure-webserver-sg

# Find SSH rule ID and delete
microstack.openstack security group rule delete <rule-id>

# Add restricted SSH rule (replace with your IP)
microstack.openstack security group rule create \
  --protocol tcp \
  --dst-port 22 \
  --remote-ip YOUR_IP_ADDRESS/32 \
  secure-webserver-sg
```

##### 17.2 Use Different Keys for Different Instances

```bash
# Create production key
microstack.openstack keypair create --private-key ~/.ssh/prod-key.pem prod-key
chmod 400 ~/.ssh/prod-key.pem

# Create development key
microstack.openstack keypair create --private-key ~/.ssh/dev-key.pem dev-key
chmod 400 ~/.ssh/dev-key.pem
```

##### 17.3 Implement Network Segmentation

Create separate security groups for different tiers:

```bash
# Web tier
microstack.openstack security group create web-tier-sg

# Application tier
microstack.openstack security group create app-tier-sg

# Database tier
microstack.openstack security group create db-tier-sg
```

Configure rules so:
- Web tier accepts HTTP/HTTPS from internet
- App tier accepts traffic only from web tier
- DB tier accepts traffic only from app tier

##### 17.4 Regular Security Audits

Create a script to audit security:

```bash
#!/bin/bash
# audit-security.sh

echo "=== Security Groups ==="
microstack.openstack security group list

echo -e "\n=== Key Pairs ==="
microstack.openstack keypair list

echo -e "\n=== Instances and Security Groups ==="
microstack.openstack server list --long

echo -e "\n=== Open Ports (0.0.0.0/0) ==="
for sg in $(microstack.openstack security group list -f value -c ID); do
    echo "Security Group: $(microstack.openstack security group show $sg -f value -c name)"
    microstack.openstack security group rule list $sg | grep "0.0.0.0/0"
done
```

Make it executable:
```bash
chmod +x audit-security.sh
./audit-security.sh
```

---

## **Practical Exercises**

### **Exercise 1: Database Server Security**

**Objective:** Create a secure database server instance

**Tasks:**
1. Create security group `database-sg`
2. Allow only port 3306 from web server IP
3. Allow SSH from admin IP only
4. Create key pair `db-admin-key`
5. Launch instance with these settings
6. Verify connectivity

**Solution:**

```bash
# Create security group
microstack.openstack security group create --description "Database server" database-sg

# Allow MySQL from web server only (replace IP)
microstack.openstack security group rule create \
  --protocol tcp --dst-port 3306 \
  --remote-ip 10.20.20.50/32 database-sg

# Allow SSH from admin IP (replace with your IP)
microstack.openstack security group rule create \
  --protocol tcp --dst-port 22 \
  --remote-ip YOUR_IP/32 database-sg

# Create key pair
microstack.openstack keypair create --private-key ~/.ssh/db-admin-key.pem db-admin-key
chmod 400 ~/.ssh/db-admin-key.pem

# Launch instance
microstack.openstack server create \
  --image cirros --flavor m1.small \
  --network test --key-name db-admin-key \
  --security-group database-sg db-server
```

### **Exercise 2: Multi-Tier Application**

**Objective:** Set up a 3-tier architecture with proper security

**Tasks:**
1. Create 3 security groups: web, app, db
2. Configure rules:
   - Web: Allow 80, 443 from internet
   - App: Allow 8080 from web tier only
   - DB: Allow 3306 from app tier only
3. Launch 3 instances (one for each tier)
4. Test connectivity between tiers

### **Exercise 3: Security Hardening**

**Objective:** Harden an existing instance

**Tasks:**
1. Audit current security groups
2. Remove overly permissive rules (0.0.0.0/0)
3. Add specific IP-based rules
4. Rotate key pairs
5. Document changes

---

## **Troubleshooting Guide**

### **Issue 1: Cannot SSH - Permission Denied**

**Error:** `Permission denied (publickey)`

**Solutions:**

1. **Check key permissions:**
   ```bash
   ls -l ~/.ssh/mykey.pem
   # Should be -r--------
   chmod 400 ~/.ssh/mykey.pem
   ```

2. **Verify correct username:**
   - Cirros: `cirros`
   - Ubuntu: `ubuntu`
   - CentOS: `centos`

3. **Check if key was added to instance:**
   ```bash
   microstack.openstack server show <instance-name> | grep key_name
   ```

4. **Use verbose SSH for debugging:**
   ```bash
   ssh -vvv -i ~/mykey.pem cirros@<ip-address>
   ```

### **Issue 2: Security Group Rules Not Working**

**Solutions:**

1. **Verify rule was added:**
   ```bash
   microstack.openstack security group rule list <security-group>
   ```

2. **Check if security group is attached to instance:**
   ```bash
   microstack.openstack server show <instance-name> | grep security_groups
   ```

3. **Ensure rule direction is correct:**
   - `ingress`: Incoming traffic
   - `egress`: Outgoing traffic

4. **Check for overlapping rules:**
   - More specific rules may be overridden by general rules

### **Issue 3: Cannot Ping Instance**

**Solutions:**

1. **Add ICMP rule:**
   ```bash
   microstack.openstack security group rule create \
     --protocol icmp <security-group>
   ```

2. **Check instance is running:**
   ```bash
   microstack.openstack server list
   ```

3. **Verify network connectivity:**
   ```bash
   microstack.openstack network list
   ```

### **Issue 4: Lost Private Key**

**Problem:** Deleted or lost private key file

**Solutions:**

1. **Cannot recover the same key pair**
   - Private keys cannot be retrieved from OpenStack

2. **Create new key pair:**
   ```bash
   microstack.openstack keypair create --private-key ~/new-key.pem new-key
   ```

3. **For existing instance:**
   - Launch new instance with new key
   - Migrate data from old instance
   - Delete old instance

4. **Prevention:**
   - Backup private keys securely
   - Use password manager or secure vault
   - Consider using SSH agent

### **Issue 5: Security Group Not Found**

**Error:** "Security group not found"

**Solutions:**

1. **List available security groups:**
   ```bash
   microstack.openstack security group list
   ```

2. **Check spelling and case:**
   - Security group names are case-sensitive

3. **Verify you're in correct project:**
   ```bash
   microstack.openstack project list
   ```

---

## **Security Checklist**

Use this checklist to ensure proper security implementation:

### **Security Groups**
- [ ] Created custom security groups (not just using default)
- [ ] Implemented principle of least privilege
- [ ] Used specific IP ranges instead of 0.0.0.0/0 where possible
- [ ] Separated rules by purpose (web, app, db)
- [ ] Documented all security group rules
- [ ] Removed unnecessary open ports
- [ ] Tested all security rules
- [ ] Regularly audit security group configurations

### **Key Pairs**
- [ ] Created unique key pairs for different purposes
- [ ] Set correct permissions (400) on private keys
- [ ] Stored private keys securely (encrypted backup)
- [ ] Never shared private keys
- [ ] Documented which key pair is used for which instance
- [ ] Tested SSH access with key pairs
- [ ] Have backup access method in case of key loss

### **Instance Security**
- [ ] All instances have security groups attached
- [ ] Instances use key-based authentication (no passwords)
- [ ] SSH restricted to specific IP addresses
- [ ] Unnecessary services disabled
- [ ] Regular security updates applied
- [ ] Monitoring enabled for failed login attempts

### **Network Security**
- [ ] Network segmentation implemented
- [ ] Private networks used for internal communication
- [ ] Floating IPs only for public-facing services
- [ ] VPN considered for administrative access

---

## **Advanced Security Features**

### **Step 18: Implementing Port Security**

Port security provides additional network-level protection.

#### 18.1 Enable Port Security

```bash
# Create port with security enabled
microstack.openstack port create \
  --network test \
  --enable-port-security \
  secure-port

# Disable port security (if needed)
microstack.openstack port set --disable-port-security secure-port
```

#### 18.2 MAC Address Filtering

```bash
# Set allowed MAC address
microstack.openstack port set \
  --allowed-address ip-address=10.20.20.100,mac-address=fa:16:3e:xx:xx:xx \
  secure-port
```

---

### **Step 19: Network Isolation**

#### 19.1 Create Private Network

```bash
# Create private network
microstack.openstack network create \
  --internal \
  private-network

# Create subnet
microstack.openstack subnet create \
  --network private-network \
  --subnet-range 192.168.100.0/24 \
  --gateway 192.168.100.1 \
  private-subnet
```

#### 19.2 Security Group for Private Network

```bash
# Create security group
microstack.openstack security group create \
  --description "Internal network only" \
  internal-sg

# Allow traffic only from private network
microstack.openstack security group rule create \
  --protocol tcp \
  --dst-port 22 \
  --remote-ip 192.168.100.0/24 \
  internal-sg
```

---

### **Step 20: Implementing Floating IP Security**

#### 20.1 Create Floating IP

```bash
# Create floating IP
microstack.openstack floating ip create external
```

#### 20.2 Associate with Instance

```bash
# Associate floating IP
microstack.openstack server add floating ip my-secure-webserver <floating-ip>
```

#### 20.3 Secure Floating IP Access

```bash
# Update security group to allow access via floating IP only
microstack.openstack security group rule create \
  --protocol tcp \
  --dst-port 22 \
  --remote-ip YOUR_PUBLIC_IP/32 \
  secure-webserver-sg
```

---

## **Security Testing and Validation**

### **Step 21: Penetration Testing Preparation**

#### 21.1 Test Port Scanning

From host machine, scan your instance:

```bash
# Install nmap if not available
sudo apt install nmap -y

# Scan instance
nmap -p 1-1000 <instance-ip>
```

**Expected result:** Only allowed ports should show as open.

#### 21.2 Test SSH Brute Force Protection

Attempt multiple failed logins:

```bash
# This should fail
ssh -i /dev/null cirros@<instance-ip>
```

Check instance logs for failed attempts:

```bash
# From inside instance
sudo grep "Failed password" /var/log/auth.log | tail -20
```

#### 21.3 Test Security Group Effectiveness

**Test blocked port:**

```bash
# Try to connect to blocked port (should timeout)
telnet <instance-ip> 3306
```

**Test allowed port:**

```bash
# Try SSH (should connect)
ssh -i ~/.ssh/mykey.pem cirros@<instance-ip>
```

---

### **Step 22: Security Compliance Check**

#### 22.1 Create Security Audit Script

Create file `security-audit.sh`:

```bash
#!/bin/bash
# OpenStack Security Audit Script

echo "================================================"
echo "OpenStack Security Audit Report"
echo "Date: $(date)"
echo "================================================"

echo -e "\n### 1. SECURITY GROUPS ###"
microstack.openstack security group list -f table

echo -e "\n### 2. OVERLY PERMISSIVE RULES (0.0.0.0/0) ###"
echo "Checking for rules allowing all IPs..."
for sg in $(microstack.openstack security group list -f value -c ID); do
    sg_name=$(microstack.openstack security group show $sg -f value -c name)
    rules=$(microstack.openstack security group rule list $sg -f value | grep "0.0.0.0/0")
    if [ ! -z "$rules" ]; then
        echo "Security Group: $sg_name"
        echo "$rules"
        echo "---"
    fi
done

echo -e "\n### 3. KEY PAIRS ###"
microstack.openstack keypair list -f table

echo -e "\n### 4. INSTANCES AND THEIR SECURITY ###"
echo "Instance Name | Status | Security Groups | Key Pair"
echo "---------------------------------------------------"
microstack.openstack server list -f value -c Name -c Status | while read name status; do
    sg=$(microstack.openstack server show "$name" -f value -c security_groups)
    key=$(microstack.openstack server show "$name" -f value -c key_name)
    echo "$name | $status | $sg | $key"
done

echo -e "\n### 5. FLOATING IPS ###"
microstack.openstack floating ip list -f table

echo -e "\n### 6. RECOMMENDATIONS ###"
echo "- Review all 0.0.0.0/0 rules and restrict to specific IPs"
echo "- Ensure all instances use key-based authentication"
echo "- Regular key rotation recommended"
echo "- Enable audit logging"
echo "- Regular security updates on instances"

echo -e "\n================================================"
echo "Audit Complete"
echo "================================================"
```

Make executable and run:

```bash
chmod +x security-audit.sh
./security-audit.sh
```

#### 22.2 Save Audit Report

```bash
./security-audit.sh > security-audit-$(date +%Y%m%d).txt
```

---

## **Real-World Security Scenarios**

### **Scenario 1: WordPress Web Application**

**Requirements:**
- Public web access (HTTP/HTTPS)
- SSH access for admin only
- MySQL database (not publicly accessible)

**Implementation:**

```bash
# 1. Create security groups
microstack.openstack security group create wordpress-web-sg
microstack.openstack security group create wordpress-db-sg

# 2. Web server rules
microstack.openstack security group rule create --protocol tcp --dst-port 80 --remote-ip 0.0.0.0/0 wordpress-web-sg
microstack.openstack security group rule create --protocol tcp --dst-port 443 --remote-ip 0.0.0.0/0 wordpress-web-sg
microstack.openstack security group rule create --protocol tcp --dst-port 22 --remote-ip YOUR_IP/32 wordpress-web-sg

# 3. Database rules (only from web server)
WEB_SERVER_IP=$(microstack.openstack server show wordpress-web -f value -c addresses | grep -oP '\d+\.\d+\.\d+\.\d+')
microstack.openstack security group rule create --protocol tcp --dst-port 3306 --remote-ip $WEB_SERVER_IP/32 wordpress-db-sg
microstack.openstack security group rule create --protocol tcp --dst-port 22 --remote-ip YOUR_IP/32 wordpress-db-sg

# 4. Launch instances
microstack.openstack keypair create --private-key ~/.ssh/wordpress-key.pem wordpress-key
chmod 400 ~/.ssh/wordpress-key.pem

microstack.openstack server create --image ubuntu --flavor m1.small --network test --key-name wordpress-key --security-group wordpress-web-sg wordpress-web

microstack.openstack server create --image ubuntu --flavor m1.small --network test --key-name wordpress-key --security-group wordpress-db-sg wordpress-db
```

---

### **Scenario 2: Development and Production Environments**

**Requirements:**
- Separate security for dev and prod
- Dev: Accessible from office network
- Prod: Strict access control

**Implementation:**

```bash
# Development environment
microstack.openstack security group create dev-sg
microstack.openstack security group rule create --protocol tcp --dst-port 22 --remote-ip 192.168.1.0/24 dev-sg
microstack.openstack security group rule create --protocol tcp --dst-port 80 --remote-ip 192.168.1.0/24 dev-sg
microstack.openstack security group rule create --protocol tcp --dst-port 8080 --remote-ip 192.168.1.0/24 dev-sg

# Production environment
microstack.openstack security group create prod-sg
microstack.openstack security group rule create --protocol tcp --dst-port 22 --remote-ip BASTION_IP/32 prod-sg
microstack.openstack security group rule create --protocol tcp --dst-port 80 --remote-ip 0.0.0.0/0 prod-sg
microstack.openstack security group rule create --protocol tcp --dst-port 443 --remote-ip 0.0.0.0/0 prod-sg

# Separate key pairs
microstack.openstack keypair create --private-key ~/.ssh/dev-key.pem dev-key
microstack.openstack keypair create --private-key ~/.ssh/prod-key.pem prod-key
chmod 400 ~/.ssh/*.pem
```

---

### **Scenario 3: Jump/Bastion Host Setup**

**Requirements:**
- Single entry point for SSH access
- All other instances accessible only via bastion

**Implementation:**

```bash
# Bastion host security group
microstack.openstack security group create bastion-sg
microstack.openstack security group rule create --protocol tcp --dst-port 22 --remote-ip YOUR_IP/32 bastion-sg

# Internal servers security group
microstack.openstack security group create internal-sg
BASTION_IP=$(microstack.openstack server show bastion -f value -c addresses | grep -oP '\d+\.\d+\.\d+\.\d+')
microstack.openstack security group rule create --protocol tcp --dst-port 22 --remote-ip $BASTION_IP/32 internal-sg

# Launch bastion
microstack.openstack server create --image ubuntu --flavor m1.small --network test --key-name bastion-key --security-group bastion-sg bastion-host

# Launch internal servers
microstack.openstack server create --image ubuntu --flavor m1.small --network test --key-name internal-key --security-group internal-sg internal-server-1
```

**Access pattern:**

```bash
# SSH to bastion
ssh -i ~/.ssh/bastion-key.pem ubuntu@<bastion-ip>

# From bastion, SSH to internal servers
ssh -i ~/.ssh/internal-key.pem ubuntu@<internal-server-ip>
```

---

## **Documentation Template**

### **Security Configuration Document**

Create a file `SECURITY-CONFIG.md`:

```markdown
# OpenStack Security Configuration

## Project Information
- **Project Name:** [Your Project]
- **Environment:** [Development/Production]
- **Date:** [Current Date]
- **Administrator:** [Your Name]

## Security Groups

### web-server-sg
**Purpose:** Public-facing web servers
**Rules:**
- TCP 80 (HTTP): 0.0.0.0/0
- TCP 443 (HTTPS): 0.0.0.0/0
- TCP 22 (SSH): 203.0.113.50/32 (Admin IP)
- ICMP: 0.0.0.0/0

### database-sg
**Purpose:** Database servers
**Rules:**
- TCP 3306 (MySQL): 10.20.20.50/32 (Web server)
- TCP 22 (SSH): 203.0.113.50/32 (Admin IP)

## Key Pairs

### Production Keys
- **prod-web-key**: Web servers (expires: 2024-12-31)
- **prod-db-key**: Database servers (expires: 2024-12-31)

### Development Keys
- **dev-key**: Development instances

## Instance Security Map

| Instance Name | Security Group | Key Pair | Purpose |
|---------------|----------------|----------|---------|
| web-server-01 | web-server-sg | prod-web-key | Production web |
| db-server-01 | database-sg | prod-db-key | Production DB |

## Audit Schedule
- Weekly: Review failed login attempts
- Monthly: Security group audit
- Quarterly: Key rotation

## Emergency Contacts
- Security Team: security@example.com
- On-call Admin: +1-555-0100
```

---

## **Command Quick Reference**

### **Security Groups**

```bash
# Create
microstack.openstack security group create <name>

# List
microstack.openstack security group list

# Show details
microstack.openstack security group show <name>

# Delete
microstack.openstack security group delete <name>

# Add rule
microstack.openstack security group rule create --protocol <tcp/udp/icmp> --dst-port <port> --remote-ip <cidr> <sg-name>

# List rules
microstack.openstack security group rule list <sg-name>

# Delete rule
microstack.openstack security group rule delete <rule-id>

# Add to instance
microstack.openstack server add security group <instance> <sg-name>

# Remove from instance
microstack.openstack server remove security group <instance> <sg-name>
```

### **Key Pairs**

```bash
# Create new key pair
microstack.openstack keypair create --private-key <path> <name>

# Import existing key
microstack.openstack keypair create --public-key <path> <name>

# List
microstack.openstack keypair list

# Show details
microstack.openstack keypair show <name>

# Delete
microstack.openstack keypair delete <name>

# Show public key
microstack.openstack keypair show --public-key <name>
```

---

## **Key Takeaways**

✅ **Security Groups** act as virtual firewalls controlling network traffic  
✅ **Key Pairs** provide secure SSH authentication without passwords  
✅ **Principle of Least Privilege** - only allow necessary access  
✅ **Network Segmentation** - separate different tiers/environments  
✅ **Regular Audits** - monitor and review security configurations  
✅ **Secure Key Storage** - protect private keys with proper permissions  
✅ **Documentation** - maintain records of security configurations  
✅ **Testing** - verify security rules work as expected  

---

## **Lab Assignment**

### **Assignment 1: Secure Multi-Tier Application**

**Objective:** Deploy a 3-tier application with proper security

**Requirements:**
1. Create 3 security groups (web, app, database)
2. Configure proper rules:
   - Web tier: HTTP/HTTPS from internet, SSH from admin IP
   - App tier: Port 8080 from web tier only, SSH from admin IP
   - DB tier: MySQL from app tier only, SSH from admin IP
3. Create separate key pairs for each tier
4. Launch 3 instances (one per tier)
5. Test connectivity between tiers
6. Document security configuration

**Deliverables:**
- Screenshot of security groups
- Screenshot of instances with security groups
- Security configuration document
- Test results showing connectivity

---

### **Assignment 2: Security Audit**

**Objective:** Audit existing OpenStack security configuration

**Tasks:**
1. List all security groups and their rules
2. Identify overly permissive rules (0.0.0.0/0)
3. Check all instances for key pair usage
4. Verify SSH access works with key pairs
5. Create recommendations report

**Deliverables:**
- Audit report with findings
- List of security issues
- Recommendations for improvement
- Remediation plan

---

### **Assignment 3: Incident Response**

**Scenario:** A key pair has been compromised

**Tasks:**
1. Identify all instances using compromised key
2. Create new key pair
3. Plan migration strategy
4. Document incident response procedure

**Deliverables:**
- List of affected instances
- New key pair creation proof
- Step-by-step migration plan
- Updated security procedures

---

## **Conclusion**

You have successfully:
- Implemented security groups with custom firewall rules
- Created and managed SSH key pairs
- Launched secure instances with proper authentication
- Applied security best practices
- Performed security audits
- Documented security configurations

OpenStack security is crucial for protecting cloud resources. The combination of security groups and key pairs provides a strong foundation for securing your cloud infrastructure. Always follow the principle of least privilege, regularly audit your configurations, and keep security documentation up to date.

---

## **Further Learning**

### **Advanced Security Topics**

1. **Barbican (Key Management Service)**
   - Secure storage for secrets
   - Encryption key management
   - Certificate management

2. **Congress (Policy as a Service)**
   - Policy enforcement
   - Compliance monitoring
   - Automated policy violations detection

3. **Neutron Advanced Security**
   - Security group logging
   - Port security features
   - Network ACLs

4. **Identity Management**
   - LDAP/Active Directory integration
   - Multi-factor authentication
   - Role-based access control (RBAC)

5. **Encryption**
   - Volume encryption
   - Object storage encryption
   - Network encryption (VPN)

---

## **References**

- [OpenStack Security Guide](https://docs.openstack.org/security-guide/)
- [Neutron Security Groups Documentation](https://docs.openstack.org/neutron/latest/admin/intro-security-groups.html)
- [Nova Key Pair Management](https://docs.openstack.org/nova/latest/user/key-pairs.html)
- [OpenStack Security Best Practices](https://wiki.openstack.org/wiki/Security)
- [NIST Cloud Security Guidelines](https://csrc.nist.gov/publications/detail/sp/800-144/final)
- [CIS OpenStack Benchmark](https://www.cisecurity.org/benchmark/openstack)

---

## **Appendix A: Common Ports Reference**

| Service | Port | Protocol | Description |
|---------|------|----------|-------------|
| SSH | 22 | TCP | Secure Shell |
| HTTP | 80 | TCP | Web traffic |
| HTTPS | 443 | TCP | Secure web traffic |
| MySQL | 3306 | TCP | MySQL database |
| PostgreSQL | 5432 | TCP | PostgreSQL database |
| MongoDB | 27017 | TCP | MongoDB database |
| Redis | 6379 | TCP | Redis cache |
| SMTP | 25 | TCP | Email |
| DNS | 53 | UDP | Domain Name System |
| NTP | 123 | UDP | Network Time Protocol |
| LDAP | 389 | TCP | Directory service |
| RDP | 3389 | TCP | Remote Desktop |
| FTP | 21 | TCP | File Transfer |

---

## **Appendix B: Security Group Examples**

### **Web Server**
```bash
microstack.openstack security group rule create --protocol tcp --dst-port 80 --remote-ip 0.0.0.0/0 web-sg
microstack.openstack security group rule create --protocol tcp --dst-port 443 --remote-ip 0.0.0.0/0 web-sg
microstack.openstack security group rule create --protocol tcp --dst-port 22 --remote-ip YOUR_IP/32 web-sg
```

### **Database Server**
```bash
microstack.openstack security group rule create --protocol tcp --dst-port 3306 --remote-ip WEB_SERVER_IP/32 db-sg
microstack.openstack security group rule create --protocol tcp --dst-port 22 --remote-ip ADMIN_IP/32 db-sg
```

### **Application Server**
```bash
microstack.openstack security group rule create --protocol tcp --dst-port 8080 --remote-ip WEB_SERVER_IP/32 app-sg
microstack.openstack security group rule create --protocol tcp --dst-port 22 --remote-ip ADMIN_IP/32 app-sg
```

---

**End of Practical**
