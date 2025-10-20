# 1) Dọn sạch hoàn toàn
rm -rf /var/lib/apt/lists/*
mkdir -p /var/lib/apt/lists/partial
rm -f /var/cache/apt/archives/*.deb
apt clean
apt autoclean

# 2) Ép APT dùng .gz, tắt pipeline, dùng IPv4 và tăng retry
cat >/etc/apt/apt.conf.d/99net-workaround <<'EOF'
Acquire::CompressionTypes::Order { "gz"; };
Acquire::http::Pipeline-Depth "0";
Acquire::Retries "5";
Acquire::http::No-Cache "true";
Acquire::ForceIPv4 "true";
EOF

# 3) (Tuỳ chọn nhưng nên làm) – sửa sources về CDN chính thức https
cat >/etc/apt/sources.list <<'EOF'
deb https://deb.debian.org/debian bookworm main contrib non-free non-free-firmware
deb https://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware
deb https://deb.debian.org/debian bookworm-updates main contrib non-free non-free-firmware
deb https://deb.debian.org/debian bookworm-backports main contrib non-free non-free-firmware
EOF

# 4) Update lại, chấp nhận đổi Release info nếu có
apt update --allow-releaseinfo-change --fix-missing
