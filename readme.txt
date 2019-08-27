
install
    [RPM]
        rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch

        cat >/etc/yum.repo.d/elasticsearch.repo <<'eof'
        [kibana-7.x]
        name=Kibana repository for 7.x packages
        baseurl=https://artifacts.elastic.co/packages/7.x/yum
        gpgcheck=1
        gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
        enabled=1
        autorefresh=1
        type=rpm-md
        <'eof'

        yum search elasticsearch
        yum search kibana

        yum install -y elasticsearch
        yum install -y kibana
    [BIN]
        wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.3.1-linux-x86_64.tar.gz

config
    https://www.elastic.co/guide/en/elasticsearch/reference/7.3/important-settings.html
    https://www.elastic.co/guide/en/elasticsearch/reference/7.3/system-config.html
    
    network.host = '0.0.0.0'
    node.name = node-1
    cluster.name = 'elasticsearch-cluster'
    cluster.initial_master_nodes: ["node-1"]
    
    sysctl -w vm.max_map_count=262144
    ulimit -n 65535
    ulimit -u 4096
    
start
    useradd elasticsearch
    sudo -u elasticsearch bin/elasticsearch