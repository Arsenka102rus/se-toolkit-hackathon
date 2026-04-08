# 🎓 University VM SSH Access Setup Guide

## Step 1: Find Your VM Information

**You need to find out:**
1. **VM address** (e.g., `vm123.student.university.edu` or an IP like `10.0.1.50`)
2. **Your username** (usually your student ID or university email prefix)
3. **How your university provides VM access** (web portal, direct SSH, etc.)

**Where to look:**
- Check your university email for VM setup instructions
- Look at your course materials/lab instructions
- Check your university's IT portal or student dashboard
- Ask your TA or classmates for the VM address pattern

**Common patterns:**
- `studentID@vm.cs.university.edu`
- `username@lab.university.edu`
- `username@IP_ADDRESS`

---

## Step 2: Generate SSH Key on Your Mac

Open Terminal and run:

```bash
# Generate SSH key (Ed25519 - modern and secure)
ssh-keygen -t ed25519 -C "your_university_email@edu.com"
```

**When prompted:**
- Press **Enter** to accept default location (`~/.ssh/id_ed25519`)
- Optionally set a passphrase (or press Enter for no passphrase)

**Check your key was created:**
```bash
ls ~/.ssh/
# You should see: id_ed25519  id_ed25519.pub
```

**View your public key:**
```bash
cat ~/.ssh/id_ed25519.pub
```

This will show something like:
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIG... your_email@edu.com
```

**COPY this entire line** - you'll need it!

---

## Step 3: Add Your Key to the VM

### Method A: If you can SSH with password

```bash
# Try to connect with password first
ssh your_username@vm_address
```

If this works, then copy your key:
```bash
ssh-copy-id your_username@vm_address
```

### Method B: If you have web portal access

Some universities provide a web interface (like Proxmox):
1. Log into the web portal
2. Find your VM
3. Look for "SSH Keys" or "Cloud-Init" section
4. Paste your public key there
5. Save and possibly restart the VM

### Method C: Manual copy

If you can SSH with password but `ssh-copy-id` doesn't work:

```bash
# 1. SSH into VM with password
ssh your_username@vm_address

# 2. On the VM, run these commands:
mkdir -p ~/.ssh
nano ~/.ssh/authorized_keys
# Paste your public key here (from Step 2)
# Save with Ctrl+X, Y, Enter

chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
exit

# 3. Now try SSH without password
ssh your_username@vm_address
```

---

## Step 4: Test SSH Connection

```bash
# Test connection
ssh your_username@vm_address

# If successful, you should see a prompt like:
# your_username@vm:~$
```

---

## Step 5: Quick Setup (Once You Have VM Access)

**Tell me your VM details and I'll give you exact commands!**

Just provide:
1. VM address (hostname or IP)
2. Your username
3. Whether you can currently SSH with password

**I'll then give you:**
- Exact commands to set up SSH keys
- Commands to deploy the bot
- Docker setup instructions

---

## Troubleshooting

### "Connection refused"
- VM might be down - check with university IT
- Wrong address - verify the VM hostname/IP

### "Permission denied (publickey)"
- Key not added to VM yet
- Wrong username
- Try: `ssh -v your_username@vm_address` for detailed error

### "Connection timed out"
- Network issue
- VM might be on different network
- Check if you need VPN access

### Still asked for password
- Key not in `authorized_keys` file
- Check permissions: `chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys`

---

## What You Need to Do NOW:

1. **Find your VM address** - Check emails, course materials, or ask TA
2. **Come back and tell me:**
   - VM address/hostname
   - Your username
   - Any access instructions you found

**Then I'll handle the rest!** 🚀
