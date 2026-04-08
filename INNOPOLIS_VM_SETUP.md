# 🎓 Innopolis University - VM SSH Access

## ✅ SSH Keys - DONE!

Your SSH keys are now properly set up:
- **Private key:** `~/.ssh/id_ed25519` (KEEP SECRET)
- **Public key:** `~/.ssh/id_ed25519.pub` (share this)

**Your Public Key:**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJCzSDzWkXsh4+MK44dKQ54XpE01J47Us/8DI5HoCCqd a.kosishnov@innopolis.university
```

---

## 🖥️ Finding Your VM Address

### Options for Innopolis Students:

**Option 1: Check Moodle/LMS**
- Go to your course page on Moodle
- Look for lab instructions or VM information
- The VM address is usually provided there

**Option 2: Check Email**
- Search your Innopolis email for "VM", "virtual machine", or "lab"
- Look for emails from IT or course instructors

**Option 3: Ask Your TA/Classmates**
- Message your TA: "What's the VM address for the SE lab?"
- Ask in your course Telegram/Discord
- Common format: `studentID@vm.innopolis.ru` or similar

**Option 4: Try Common Patterns**
```bash
# Try these (replace with your student ID):
ssh your_student_id@vm.innopolis.ru
ssh your_student_id@lab.innopolis.ru
ssh a.kosishnov@vm.innopolis.ru
```

---

## 🔑 Adding Your Key to the VM

### Method A: SSH with Password (if available)

If you can SSH with your Innopolis credentials:

```bash
# Try connecting with password
ssh your_username@VM_ADDRESS

# If it asks for password and works, copy your key:
ssh-copy-id your_username@VM_ADDRESS
```

### Method B: Manual Setup (if you have VM access)

If you already have VM credentials:

```bash
# 1. SSH into VM with password
ssh your_username@VM_ADDRESS

# 2. On the VM, run:
mkdir -p ~/.ssh
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJCzSDzWkXsh4+MK44dKQ54XpE01J47Us/8DI5HoCCqd a.kosishnov@innopolis.university" >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
exit

# 3. Now try SSH without password
ssh your_username@VM_ADDRESS
```

### Method C: Web Portal (if Innopolis uses one)

Some universities provide a web interface:
1. Check if there's an Innopolis IT portal
2. Log in with your credentials
3. Look for "SSH Keys" or "Access" section
4. Paste your public key there

---

## 📋 What You Need To Do NOW:

### Step 1: Find VM Address ⚡ URGENT
**Choose ONE:**
- [ ] Check Moodle/course page
- [ ] Search your email
- [ ] Ask TA in person/Telegram
- [ ] Ask a classmate

### Step 2: Tell Me
Once you have the VM address, tell me:
1. **VM address** (e.g., `vm.innopolis.ru` or IP)
2. **Your username** (student ID or email)
3. **Can you SSH with password?** (yes/no/don't know)

### Step 3: I'll Handle The Rest
I'll give you exact commands to:
- Add your SSH key
- Test connection
- Deploy your bot

---

## 🧪 Quick Test Commands

Once you have VM address, try:

```bash
# Test 1: Can you reach the VM?
ping VM_ADDRESS

# Test 2: Try SSH connection
ssh -v your_username@VM_ADDRESS

# Test 3: If password auth works
ssh your_username@VM_ADDRESS
```

---

## ❓ Common Innopolis VM Patterns

Based on common university setups, try asking your TA about:

- **VM Host:** Is it `vm.innopolis.ru` or a different address?
- **Username:** Is it your student ID or email prefix?
- **Access:** Do you need to request VM access first?
- **Port:** Is it standard (22) or custom?

---

## 🚀 Once You Have VM Access:

I'll deploy your bot with these commands on the VM:

```bash
# What I'll help you run on the VM:
git clone YOUR_REPO se-toolkit-hackathon
cd se-toolkit-hackathon
cp .env.example .env
# Add your Telegram token
sudo docker compose up -d
```

**Simple and fast!** But first, we need that VM address! 🎯

---

**NEXT ACTION:** Find your VM address from Moodle, email, TA, or classmates!
