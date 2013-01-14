import os
import re

#/etc/sysconfig/network-scripts/ifcfg-eth0


class Ifcfg(object):
    
    
    def __init__(self, iface):
        
        self.iface = iface
        self.filename = "ifcfg-" + iface
        self.basepath = "/home/jasonviloria/tmp/"  
        #self.basepath = "/etc/sysconfig/network-scripts/"
        self.path = os.path.join(self.basepath, self.filename)
        self.entries = {}
        self.captioned_values = False
    
    def load_config(self):
        
        with open(self.path) as f:
            
            lines = f.readlines()

        r = re.compile("(.*)=(.*)")
            
        for i in lines:
            m = r.match(i)
            if m is not None:
                key = m.group(1)
                value = m.group(2)
                t = str("h")
                if value.startswith("\"") and value.endswith("\""):
                    value = value.rstrip("\"")
                    value = value.lstrip("\"")
                    self.captioned_values = True
                    
                #print "key: {} value: {}".format(m.group(1), m.group(2))
                
                self.entries.update({key: value,})
    
               

    def __str__(self):

        lines = ""
        for key in self.entries:
            if self.captioned_values:
                tmpl = "{}=\"{}\""
            else:
                tmpl = "{}={}"
            l = tmpl.format(key, self.entries[key])
            lines = lines + l + "\n"
        
        return lines
    
    def change_entry(self, key, value):
        
        self.entries[key] = value
        
    def change_ip(self, value):
        
        key = "IPADDR"
        self.entries[key] = value
        
        if "GATEWAY" in self.entries:
            
            dq = value.split(".")
            
            gw = "{}.{}.{}.254".format(dq[0], dq[1], dq[2])
            self.entries["GATEWAY"] = gw
            
    
class Network(object):
    
    def __init__(self):
        
        self.path = "/etc/sysconfig/network"
        self.entries = {}
        
    def load_config(self):
        
        with open(self.path) as f:
            
            lines = f.readlines()
            
        pattern =  "(.*)=(.*)"
        r = re.compile(pattern)
        
        for i in lines:
            m = r.match(i)
            if m is not None:
                key = m.group(1)
                value = m.group(2)

                self.entries.update({key: value,})
                
    def __str__(self):
        
        lines = ""
        for key in self.entries:
            tmpl = "{}={}"
            l = tmpl.format(key, self.entries[key])
            lines = lines + l + "\n"
        return lines
    
    
    
def update_sshd(new_ip):
    import socket
    current_ip = socket.gethostbyname(socket.gethostname())    
    
    with open("/etc/ssh/sshd_config") as f:
        sshd_config = f.read()
        
    updated_sshd_config = re.sub(current_ip, new_ip, sshd_config)
    
    return updated_sshd_config
    
    
    
    
if __name__ == "__main__":
    
    x = Ifcfg("eth1")
    x.load_config()
    print x.entries
    print x
    x.change_ip("192.168.100.4")
    print x
    
    y = Network()
    y.load_config()
    print y
    
    print update_sshd("10.10.103.102")
    