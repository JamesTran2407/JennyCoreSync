cat >/etc/apt/apt.conf.d/99no-translations <<'EOF'
Acquire::Languages "none";
EOF

# 2) Dọn sạch index cũ
rm -rf /var/lib/apt/lists/*
mkdir -p /var/lib/apt/lists/partial
apt clean

# 3) Update lại (thêm retry + IPv4 cho chắc)
apt-get -o Acquire::Retries=5 -o Acquire::ForceIPv4=true update