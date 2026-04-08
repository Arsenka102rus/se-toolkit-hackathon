#!/bin/bash

echo "🔑 SSH Key Generator for University VM"
echo "======================================"
echo ""

# Check if SSH key already exists
if [ -f ~/.ssh/id_ed25519.pub ]; then
    echo "✅ You already have an SSH key!"
    echo ""
    echo "Your public key:"
    echo "----------------"
    cat ~/.ssh/id_ed25519.pub
    echo "----------------"
    echo ""
    echo "📋 Copy the line above and add it to your university VM"
else
    echo "🔐 Generating new SSH key..."
    echo ""
    echo "Enter your university email (or just press Enter to skip):"
    read email
    
    if [ -z "$email" ]; then
        email="student@university.edu"
    fi
    
    ssh-keygen -t ed25519 -C "$email"
    
    if [ -f ~/.ssh/id_ed25519.pub ]; then
        echo ""
        echo "✅ SSH key created!"
        echo ""
        echo "Your public key:"
        echo "----------------"
        cat ~/.ssh/id_ed25519.pub
        echo "----------------"
        echo ""
        echo "📋 COPY THIS ENTIRE LINE - you'll need it for your VM!"
    else
        echo "❌ Key generation failed. Please try manually:"
        echo "   ssh-keygen -t ed25519"
    fi
fi

echo ""
echo "📖 Next steps:"
echo "1. Find your university VM address (check emails/course materials)"
echo "2. Add this public key to your VM"
echo "3. Test with: ssh your_username@vm_address"
echo ""
echo "See VM_SSH_SETUP.md for detailed instructions"
