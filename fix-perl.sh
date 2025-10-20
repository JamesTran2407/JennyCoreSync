# 1️⃣ Dọn sạch toàn bộ APT list và cache
rm -rf /var/lib/apt/lists/*
mkdir -p /var/lib/apt/lists/partial
rm -rf /var/cache/apt/archives/*
rm -rf /var/cache/apt/pkgcache.bin /var/cache/apt/srcpkgcache.bin
apt clean
apt autoclean

# 2️⃣ Rebuild lại cấu trúc APT
dpkg --clear-avail
dpkg --configure -a

# 3️⃣ Đảm bảo file sources.list chuẩn
cat >/etc/apt/sources.list <<'EOF'
deb http://deb.debian.org/debian bookworm main contrib non-free non-free-firmware
deb http://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware
deb http://deb.debian.org/debian bookworm-updates main contrib non-free non-free-firmware
deb http://deb.debian.org/debian bookworm-backports main contrib non-free non-free-firmware
EOF

# 4️⃣ Tạo file fix cấu hình mạng apt (tắt pipeline và ép IPv4)
cat >/etc/apt/apt.conf.d/99fix.conf <<'EOF'
Acquire::http::Pipeline-Depth "0";
Acquire::Retries "5";
Acquire::ForceIPv4 "true";
Acquire::CompressionTypes::Order { "gz"; };
EOF

# 5️⃣ Rebuild APT index
apt-get clean
apt-get update -o Acquire::CompressionTypes::Order::=gz --fix-missing
