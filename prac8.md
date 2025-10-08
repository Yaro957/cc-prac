# 🧪 Practical No. 8 — Installation of OpenStack (MicroStack) as IaaS

## Complete Step-by-Step Guide

---

## **Aim**

To install and configure OpenStack using MicroStack as a single-node cloud environment and launch a test virtual machine instance.

---

## **Theory**

### What is OpenStack?

**OpenStack** is an open-source cloud computing platform that provides Infrastructure as a Service (IaaS). It allows you to create and manage large groups of virtual machines, storage, and networking resources through a web-based dashboard or command-line interface.

**Key Components:**
- **Nova:** Compute service (manages virtual machines)
- **Neutron:** Networking service (manages networks and IP addresses)
- **Glance:** Image service (manages VM images)
- **Cinder:** Block storage service (manages volumes)
- **Keystone:** Identity service (authentication and authorization)
- **Horizon:** Dashboard (web-based user interface)

### What is MicroStack?

**MicroStack** is a lightweight, single-node OpenStack deployment tool developed by Canonical. It packages OpenStack into a snap package for easy installation and management.

**Advantages of MicroStack:**
- ✅ **Quick deployment:** Install OpenStack in minutes instead of hours
- ✅ **Single-node setup:** Run on a single machine (ideal for testing/learning)
- ✅ **Automated configuration:** Minimal manual configuration required
- ✅ **Snap-based:** Easy to install, update, and remove
- ✅ **Resource efficient:** Lower resource requirements than full OpenStack

### What is IaaS?

**Infrastructure as a Service (IaaS)** is a cloud computing model that provides virtualized computing resources over the internet.

**IaaS provides:**
- Virtual machines (compute)
- Storage (block and object storage)
- Networking (virtual networks, load balancers)
- Self-service portal for resource management

---

## **System Requirements**

| Component | Minimum Requirement | Recommended |
|-----------|---------------------|-------------|
| **OS** | Ubuntu 20.04 / 22.04 / Kali Linux (64-bit) | Ubuntu Server 22.04 LTS |
| **CPU** | 4 cores | 4+ cores (8 cores ideal) |
| **RAM** | 8 GB | 16 GB or more |
| **Storage** | 80 GB free space | 100+ GB SSD |
| **Internet** | Required for package download | Stable broadband connection |
| **Virtualization** | CPU with VT-x/AMD-V support enabled | Hardware virtualization enabled in BIOS |

### Verify System Requirements

Before starting, verify your system meets the requirements:

```bash
# Check CPU cores
nproc

# Check RAM (in GB)
free -h

# Check disk space
df -h

# Check virtualization support (should show vmx or svm)
egrep -o 'vmx|svm' /proc/cpuinfo

# Check Ubuntu version
lsb_release -a
```

---

## **Complete Procedure**

### **Step 1: Prepare Your System**

#### 1.1 Update System Packages

Open Terminal and run:

```bash
sudo apt update
sudo apt upgrade -y
```

This ensures all system packages are up to date.

#### 1.2 Install Required Dependencies

Install snapd (if not already installed):

```bash
sudo apt install snapd -y
```

Verify snap installation:

```bash
snap --version
```

**Expected output:**
```
snap    2.xx.x
snapd   2.xx.x
series  16
ubuntu  22.04
kernel  5.xx.x-xx-generic
```

#### 1.3 Enable and Start Snap Service

```bash
sudo systemctl enable snapd
sudo systemctl start snapd
```

#### 1.4 Verify Virtualization Support

Check if hardware virtualization is enabled:

```bash
kvm-ok
```

**If kvm-ok is not installed:**

```bash
sudo apt install cpu-checker -y
kvm-ok
```

**Expected output:**
```
INFO: /dev/kvm exists
KVM acceleration can be used
```

**If you see an error:** You need to enable VT-x/AMD-V in your BIOS settings.

---

### **Step 2: Install MicroStack**

#### 2.1 Install MicroStack Snap Package

Install MicroStack using snap:

```bash
sudo snap install microstack --beta
```

**Note:** We use `--beta` channel for the latest stable features. You can also use `--edge` for the latest development version.

**Installation time:** 5-10 minutes depending on your internet speed.

**Expected output:**
```
microstack (beta) xxxxxx from Canonical✓ installed
```

#### 2.2 Verify Installation

Check if MicroStack is installed:

```bash
snap list microstack
```

**Expected output:**
```
Name        Version    Rev   Tracking       Publisher   Notes
microstack  ussuri     xxx   beta           canonical✓  -
```

#### 2.3 Check MicroStack Status

```bash
microstack.openstack --version
```

This confirms the OpenStack CLI is available.

---

### **Step 3: Initialize MicroStack**

#### 3.1 Run Initialization

Initialize MicroStack with default settings:

```bash
sudo microstack init --auto --control
```

**What this does:**
- Sets up all OpenStack services
- Configures networking
- Creates default flavors (VM sizes)
- Downloads a test image (Cirros)
- Creates default security groups
- Generates admin credentials

**Initialization time:** 10-15 minutes

**Expected output:**
```
2024-XX-XX XX:XX:XX - INFO - Configuring clustering ...
2024-XX-XX XX:XX:XX - INFO - Configuring networking ...
2024-XX-XX XX:XX:XX - INFO - Configuring OpenStack services ...
2024-XX-XX XX:XX:XX - INFO - Creating default flavors ...
2024-XX-XX XX:XX:XX - INFO - Downloading Cirros image ...
2024-XX-XX XX:XX:XX - INFO - Complete. You can now access the OpenStack dashboard
```

#### 3.2 Troubleshooting Initialization

**If initialization fails:**

1. **Check logs:**
   ```bash
   sudo journalctl -u snap.microstack.*
   ```

2. **Restart services:**
   ```bash
   sudo snap restart microstack
   ```

3. **Re-initialize:**
   ```bash
   sudo microstack init --auto --control
   ```

---

### **Step 4: Access OpenStack Dashboard (Horizon)**

#### 4.1 Get Admin Credentials

After initialization, get the admin password:

```bash
sudo snap get microstack config.credentials.keystone-password
```

**Example output:**
```
randomGeneratedPassword123
```

**Save this password!** You'll need it to log in.

#### 4.2 Access the Dashboard

Open your web browser and navigate to:

```
http://localhost
```

Or use your machine's IP address:

```
http://<your-ip-address>
```

To find your IP address:

```bash
hostname -I
```

#### 4.3 Log In to Horizon

**Login credentials:**
- **Username:** `admin`
- **Password:** (use the password from Step 4.1)
- **Domain:** `Default`

**Horizon Dashboard Interface:**
- **Left sidebar:** Navigation menu
- **Main panel:** Resource overview and management
- **Top right:** User settings and project selector

---

### **Step 5: Launch a Test Virtual Machine**

#### 5.1 Via Command Line (Recommended for First Time)

##### 5.1.1 List Available Images

```bash
microstack.openstack image list
```

**Expected output:**
```
+--------------------------------------+--------+--------+
| ID                                   | Name   | Status |
+--------------------------------------+--------+--------+
| xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | cirros | active |
+--------------------------------------+--------+--------+
```

##### 5.1.2 List Available Flavors (VM Sizes)

```bash
microstack.openstack flavor list
```

**Expected output:**
```
+----+-----------+-------+------+
| ID | Name      | RAM   | Disk |
+----+-----------+-------+------+
| 1  | m1.tiny   | 512   | 1    |
| 2  | m1.small  | 2048  | 20   |
| 3  | m1.medium | 4096  | 40   |
| 4  | m1.large  | 8192  | 80   |
+----+-----------+-------+------+
```

##### 5.1.3 List Available Networks

```bash
microstack.openstack network list
```

**Expected output:**
```
+--------------------------------------+---------+
| ID                                   | Name    |
+--------------------------------------+---------+
| xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | test    |
| xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | external|
+--------------------------------------+---------+
```

##### 5.1.4 Create Security Group Rule (Allow SSH)

Allow SSH access to your VM:

```bash
microstack.openstack security group rule create --proto tcp --dst-port 22 default
```

Allow ICMP (ping):

```bash
microstack.openstack security group rule create --proto icmp default
```

##### 5.1.5 Launch the VM Instance

```bash
microstack launch cirros --name test-vm --flavor m1.small --key-name mykey
```

**Alternative (if above doesn't work):**

```bash
microstack.openstack server create \
  --image cirros \
  --flavor m1.small \
  --network test \
  test-vm
```

**Expected output:**
```
Server test-vm launched! (status is BUILD)
Access it with `ssh -i /path/to/key cirros@<ip-address>`
```

##### 5.1.6 Check VM Status

```bash
microstack.openstack server list
```

**Expected output:**
```
+--------------------------------------+---------+--------+
| ID                                   | Name    | Status |
+--------------------------------------+---------+--------+
| xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | test-vm | ACTIVE |
+--------------------------------------+---------+--------+
```

Wait until Status shows **ACTIVE** (may take 1-2 minutes).

##### 5.1.7 Get VM Details

```bash
microstack.openstack server show test-vm
```

This displays full VM information including IP address, flavor, image, etc.

#### 5.2 Via Web Dashboard (Horizon)

##### 5.2.1 Navigate to Instances

1. Log in to Horizon dashboard
2. Go to **Project → Compute → Instances**
3. Click **Launch Instance** button

##### 5.2.2 Configure Instance Details

**Details Tab:**
- **Instance Name:** `test-vm-web`
- **Description:** (optional) "Test VM created via Horizon"
- **Availability Zone:** `nova`
- **Count:** `1`

Click **Next**

##### 5.2.3 Select Source Image

**Source Tab:**
- **Select Boot Source:** `Image`
- **Create New Volume:** `No`
- **Allocated:** Click the **↑** arrow next to `cirros` image

Click **Next**

##### 5.2.4 Select Flavor

**Flavor Tab:**
- **Allocated:** Click the **↑** arrow next to `m1.small`

Click **Next**

##### 5.2.5 Select Network

**Networks Tab:**
- **Allocated:** Click the **↑** arrow next to `test` network

Click **Next**

##### 5.2.6 Configure Security Groups

**Security Groups Tab:**
- Ensure **default** is in Allocated section

Click **Next**

##### 5.2.7 Key Pair (Optional)

**Key Pair Tab:**
- Skip for now (or create a new key pair if needed)

Click **Launch Instance**

##### 5.2.8 Monitor Instance Creation

The Instances page will show your new VM:
- **Status:** `Build` → `Active` (wait 1-2 minutes)
- **Power State:** `Running`
- **IP Address:** Will be assigned automatically

---

### **Step 6: Access and Test the Virtual Machine**

#### 6.1 Get VM Console Access

##### Via Command Line:

```bash
microstack.openstack console url show test-vm
```

Copy the URL and open it in your browser to access the VM console.

##### Via Horizon Dashboard:

1. Go to **Project → Compute → Instances**
2. Click on your VM name (`test-vm`)
3. Go to **Console** tab
4. You'll see a terminal interface

#### 6.2 Log In to VM

**Default Cirros credentials:**
- **Username:** `cirros`
- **Password:** `gocubsgo`

Type these credentials in the console.

#### 6.3 Test VM Connectivity

Once logged in, run these commands inside the VM:

```bash
# Check IP address
ip addr show

# Test internet connectivity
ping -c 3 8.8.8.8

# Check hostname
hostname

# Display system info
uname -a
```

#### 6.4 Test from Host Machine

Get the VM's IP address:

```bash
microstack.openstack server show test-vm -f value -c addresses
```

Example output: `test=10.20.20.xx`

Ping the VM from your host:

```bash
ping <vm-ip-address>
```

---

### **Step 7: Manage Virtual Machine Instances**

#### 7.1 Stop (Pause) an Instance

```bash
microstack.openstack server stop test-vm
```

#### 7.2 Start a Stopped Instance

```bash
microstack.openstack server start test-vm
```

#### 7.3 Reboot an Instance

```bash
microstack.openstack server reboot test-vm
```

#### 7.4 Delete an Instance

```bash
microstack.openstack server delete test-vm
```

**Confirm deletion:**

```bash
microstack.openstack server list
```

The VM should no longer appear in the list.

#### 7.5 Create a Snapshot

Create a snapshot of a running VM:

```bash
microstack.openstack server image create --name test-vm-snapshot test-vm
```

View snapshots:

```bash
microstack.openstack image list
```

---

### **Step 8: Working with Images**

#### 8.1 List All Images

```bash
microstack.openstack image list
```

#### 8.2 Download Additional Images

Download Ubuntu Cloud Image:

```bash
wget https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img
```

#### 8.3 Upload Image to Glance

```bash
microstack.openstack image create \
  --file focal-server-cloudimg-amd64.img \
  --disk-format qcow2 \
  --container-format bare \
  --public \
  ubuntu-20.04
```

#### 8.4 Verify Image Upload

```bash
microstack.openstack image list
```

Now you can launch VMs using this Ubuntu image.

---

### **Step 9: Networking Configuration**

#### 9.1 List Networks

```bash
microstack.openstack network list
```

#### 9.2 Create a New Network

```bash
microstack.openstack network create my-network
```

#### 9.3 Create Subnet

```bash
microstack.openstack subnet create \
  --network my-network \
  --subnet-range 192.168.100.0/24 \
  my-subnet
```

#### 9.4 Create Router

```bash
microstack.openstack router create my-router
```

#### 9.5 Attach Router to Subnet

```bash
microstack.openstack router add subnet my-router my-subnet
```

#### 9.6 Set External Gateway

```bash
microstack.openstack router set --external-gateway external my-router
```

---

### **Step 10: Storage Management**

#### 10.1 Create a Volume

```bash
microstack.openstack volume create --size 10 my-volume
```

#### 10.2 List Volumes

```bash
microstack.openstack volume list
```

#### 10.3 Attach Volume to Instance

```bash
microstack.openstack server add volume test-vm my-volume
```

#### 10.4 Detach Volume

```bash
microstack.openstack server remove volume test-vm my-volume
```

#### 10.5 Delete Volume

```bash
microstack.openstack volume delete my-volume
```

---

## **Common MicroStack Commands Reference**

### Service Management

```bash
# Restart all MicroStack services
sudo snap restart microstack

# Stop all services
sudo snap stop microstack

# Start all services
sudo snap start microstack

# Check service status
sudo snap services microstack
```

### OpenStack CLI

```bash
# General format
microstack.openstack <service> <action> <options>

# Get help
microstack.openstack --help

# Service-specific help
microstack.openstack server --help
```

### Configuration

```bash
# Get configuration values
sudo snap get microstack

# Set configuration values
sudo snap set microstack <key>=<value>
```

---

## **Troubleshooting Guide**

### **Issue 1: Initialization Fails**

**Error:** "Failed to initialize MicroStack"

**Solutions:**
1. Check system resources (RAM, CPU, disk space)
   ```bash
   free -h
   df -h
   nproc
   ```
2. Ensure virtualization is enabled
   ```bash
   kvm-ok
   ```
3. Check for conflicting services (other OpenStack installations)
4. Re-initialize with verbose output
   ```bash
   sudo microstack init --auto --control --debug
   ```

### **Issue 2: Cannot Access Dashboard**

**Error:** "Unable to connect" when accessing localhost

**Solutions:**
1. Check if services are running
   ```bash
   sudo snap services microstack
   ```
2. Restart services
   ```bash
   sudo snap restart microstack
   ```
3. Check firewall rules
   ```bash
   sudo ufw status
   sudo ufw allow 80/tcp
   ```
4. Try accessing via IP address instead of localhost

### **Issue 3: VM Fails to Launch**

**Error:** "No valid host was found"

**Solutions:**
1. Check available resources
   ```bash
   microstack.openstack hypervisor stats show
   ```
2. Use smaller flavor
   ```bash
   microstack.openstack server create --flavor m1.tiny ...
   ```
3. Check compute service
   ```bash
   microstack.openstack compute service list
   ```

### **Issue 4: No Internet in VM**

**Solutions:**
1. Check network configuration
   ```bash
   microstack.openstack network list
   ```
2. Verify router configuration
   ```bash
   microstack.openstack router list
   ```
3. Check security group rules
   ```bash
   microstack.openstack security group rule list default
   ```

### **Issue 5: Snap Installation Issues**

**Error:** "snap not found" or similar

**Solutions:**
1. Install snapd
   ```bash
   sudo apt install snapd -y
   ```
2. Reload snap environment
   ```bash
   sudo systemctl restart snapd
   ```
3. Log out and log back in

---

## **Verification and Testing Checklist**

Use this checklist to verify your installation:

- [ ] MicroStack snap installed successfully
- [ ] Initialization completed without errors
- [ ] Dashboard accessible at http://localhost
- [ ] Can log in with admin credentials
- [ ] Cirros image available in image list
- [ ] Default flavors (m1.tiny, m1.small, etc.) exist
- [ ] Default network created
- [ ] Successfully launched test VM via CLI
- [ ] Successfully launched test VM via Horizon
- [ ] VM status shows ACTIVE
- [ ] VM has IP address assigned
- [ ] Can access VM console
- [ ] Can log in to VM
- [ ] VM can ping external addresses
- [ ] Can create snapshots
- [ ] Can stop/start/reboot VM
- [ ] Can delete VM

---

## **Uninstalling MicroStack**

If you need to remove MicroStack:

### Remove MicroStack Snap

```bash
sudo snap remove --purge microstack
```

### Clean Up Remaining Files

```bash
sudo rm -rf /var/snap/microstack
sudo rm -rf ~/snap/microstack
```

---

## **Best Practices**

1. **Resource Allocation:**
   - Allocate at least 16GB RAM for better performance
   - Use SSD storage for better VM performance
   - Don't overcommit resources

2. **Security:**
   - Change default admin password
   - Create separate user accounts for different projects
   - Use security groups to control access
   - Keep MicroStack updated

3. **Networking:**
   - Plan your network topology before creating resources
   - Use meaningful names for networks and subnets
   - Document your network configuration

4. **Instance Management:**
   - Use descriptive names for instances
   - Tag instances for better organization
   - Create snapshots before major changes
   - Clean up unused instances

5. **Monitoring:**
   - Regularly check service status
   - Monitor resource usage
   - Review logs for errors
   - Keep track of quotas

---

## **Additional Resources and Commands**

### Useful Commands

```bash
# View all OpenStack services
microstack.openstack service list

# View all projects
microstack.openstack project list

# View all users
microstack.openstack user list

# View resource quotas
microstack.openstack quota show

# View system limits
microstack.openstack limits show

# View availability zones
microstack.openstack availability zone list

# View hypervisor stats
microstack.openstack hypervisor stats show
```

### Log Files

```bash
# View all MicroStack logs
sudo journalctl -u snap.microstack.*

# View specific service logs
sudo journalctl -u snap.microstack.nova-compute

# Follow logs in real-time
sudo journalctl -u snap.microstack.* -f
```

---

## **Key Takeaways**

✅ **OpenStack** is a powerful open-source cloud platform for IaaS  
✅ **MicroStack** simplifies OpenStack deployment to a single command  
✅ OpenStack provides **compute, storage, and networking** as a service  
✅ **Horizon dashboard** offers web-based management  
✅ **CLI tools** provide automation capabilities  
✅ **Cirros** is a lightweight test image perfect for learning  
✅ Virtual machines can be managed via **CLI or web interface**  
✅ MicroStack is ideal for **learning, testing, and development**  

---

## **Conclusion**

You have successfully:
- Installed MicroStack on Ubuntu
- Initialized a single-node OpenStack environment
- Accessed the Horizon dashboard
- Launched and managed virtual machine instances
- Understood basic OpenStack concepts and components
- Learned to manage compute, storage, and networking resources

MicroStack provides a complete IaaS platform that demonstrates cloud computing principles. This setup can be used for learning, testing applications, and understanding cloud infrastructure management.

---

## **What's Next?**

### Advanced Topics to Explore:

1. **Multi-node deployment:** Set up OpenStack across multiple machines
2. **Custom flavors:** Create VM sizes for specific workloads
3. **Heat templates:** Use orchestration for automated deployments
4. **Object storage:** Implement Swift for object storage
5. **Load balancing:** Set up Octavia for load balancing
6. **Monitoring:** Integrate monitoring tools like Prometheus
7. **Automation:** Use Ansible or Terraform with OpenStack

---

## **References**

- [MicroStack Official Documentation](https://microstack.run/docs)
- [OpenStack Official Documentation](https://docs.openstack.org/)
- [Canonical OpenStack](https://ubuntu.com/openstack)
- [OpenStack CLI Reference](https://docs.openstack.org/python-openstackclient/latest/)
- [Cirros Test Image](https://docs.openstack.org/image-guide/obtain-images.html)

---

**End of Practical**
