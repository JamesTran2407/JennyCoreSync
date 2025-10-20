#!/bin/bash
set -e
echo "🔧 Cleaning up old cache..."
rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*.deb
apt clean

echo "🌀 Updating sources..."
cat >/etc/apt/sources.list <<'EOF'
deb https://deb.debian.org/debian bookworm main contrib non-free non-free-firmware
deb https://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware
deb https://deb.debian.org/debian bookworm-updates main contrib non-free non-free-firmware
deb https://deb.debian.org/debian bookworm-backports main contrib non-free non-free-firmware
EOF

echo "📦 Updating and reinstalling Perl..."
apt update --allow-releaseinfo-change --fix-missing
apt-get -o Acquire::Retries=5 -o Acquire::http::Pipeline-Depth=0 install --reinstall perl perl-base perl-modules-5.36 libperl5.36 -y || true
apt --fix-broken install -y
apt upgrade -y
apt autoremove -y

echo "✅ Done. Checking Perl version..."
perl -v
