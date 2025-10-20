rm -rf /var/lib/apt/lists/*
mkdir -p /var/lib/apt/lists/partial
echo 'Acquire::CompressionTypes::Order { "gz"; };' > /etc/apt/apt.conf.d/99gz.conf
apt-get -o Acquire::CompressionTypes::Order::=gz update
