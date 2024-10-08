import csv
from collections import defaultdict

# protocol_lookup generated using protocol_lookup.py
protocol_lookup = {"0": "hopopt", "1": "icmp", "2": "igmp", "3": "ggp", "4": "ipv4", "5": "st", "6": "tcp", "7": "cbt", "8": "egp",
                   "9": "igp", "10": "bbn-rcc-mon", "11": "nvp-ii", "12": "pup", "13": "argus", "14": "emcon", "15": "xnet", 
                   "16": "chaos", "17": "udp", "18": "mux", "19": "dcn-meas", "20": "hmp", "21": "prm", "22": "xns-idp", "23": "trunk-1", 
                   "24": "trunk-2", "25": "leaf-1", "26": "leaf-2", "27": "rdp", "28": "irtp", "29": "iso-tp4", "30": "netblt", 
                   "31": "mfe-nsp", "32": "merit-inp", "33": "dccp", "34": "3pc", "35": "idpr", "36": "xtp", "37": "ddp", 
                   "38": "idpr-cmtp", "39": "tp++", "40": "il", "41": "ipv6", "42": "sdrp", "43": "ipv6-route", "44": "ipv6-frag",
                   "45": "idrp", "46": "rsvp", "47": "gre", "48": "dsr", "49": "bna", "50": "esp", "51": "ah", "52": "i-nlsp", 
                   "53": "swipe", "54": "narp", "55": "min-ipv4", "56": "tlsp", "57": "skip", "58": "ipv6-icmp", "59": "ipv6-nonxt", 
                   "60": "ipv6-opts", "62": "cftp", "64": "sat-expak", "65": "kryptolan", "66": "rvd", "67": "ippc", "69": "sat-mon", 
                   "70": "visa", "71": "ipcv", "72": "cpnx", "73": "cphb", "74": "wsn", "75": "pvp", "76": "br-sat-mon", "77": "sun-nd", 
                   "78": "wb-mon", "79": "wb-expak", "80": "iso-ip", "81": "vmtp", "82": "secure-vmtp", "83": "vines", "84": "iptm", 
                   "85": "nsfnet-igp", "86": "dgp", "87": "tcf", "88": "eigrp", "89": "ospfigp", "90": "sprite-rpc", "91": "larp", 
                   "92": "mtp", "93": "ax.25", "94": "ipip", "95": "micp ", "96": "scc-sp", "97": "etherip", "98": "encap", "100": "gmtp", 
                   "101": "ifmp", "102": "pnni", "103": "pim", "104": "aris", "105": "scps", "106": "qnx", "107": "a/n", "108": "ipcomp", 
                   "109": "snp", "110": "compaq-peer", "111": "ipx-in-ip", "112": "vrrp", "113": "pgm", "115": "l2tp", "116": "ddx", 
                   "117": "iatp", "118": "stp", "119": "srp", "120": "uti", "121": "smp", "122": "sm", "123": "ptp", "124": "isis over ipv4", 
                   "125": "fire", "126": "crtp", "127": "crudp", "128": "sscopmce", "129": "iplt", "130": "sps", "131": "pipe", "132": "sctp", 
                   "133": "fc", "134": "rsvp-e2e-ignore", "135": "mobility header", "136": "udplite", "137": "mpls-in-ip", "138": "manet", 
                   "139": "hip", "140": "shim6", "141": "wesp", "142": "rohc", "143": "ethernet", "144": "aggfrag", "145": "nsh", "888":"new protocol"}

# Function to load the lookup table into a dictionary
def load_lookup_table(lookup_file):
    lookup_dict = {}
    with open(lookup_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = (int(row['dstport']), row['protocol'].lower())
            lookup_dict[key] = row['tag']  
    return lookup_dict

# Function to parse the flow log file and count matches
def process_flow_logs(flow_log_file, lookup_dict):
    tag_count = defaultdict(int)
    port_protocol_count = defaultdict(int)
    with open(flow_log_file, mode='r') as file:
        for line in file:
            parts = line.strip().split()
            # Checking if the entry is Valid
            if len(parts) < 8:
                continue

            dstport = int(parts[6])
            protocol_code = parts[7]
            if protocol_code in protocol_lookup:
                protocol = protocol_lookup[protocol_code]
            else:
                protocol = "Undefined Protocol"  

            key = (dstport, protocol)
            if key in lookup_dict:
                tag = lookup_dict[key]
            else:
                tag = "Untagged"

            port_protocol_count[(dstport, protocol)] += 1    
            tag_count[tag] += 1

    return tag_count, port_protocol_count

# Function to write the results to output files
def generate_output_files(tag_count, port_protocol_count):
    with open('tag_count.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Tag", "Count"])
        for tag, count in tag_count.items():
            writer.writerow([tag, count])
    
    with open('port_protocol_count.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Port", "Protocol", "Count"])
        for (port, protocol), count in port_protocol_count.items():
            writer.writerow([port, protocol, count])

# Main function to run the program
def main():
    lookup_file = 'Test_Files/lookup_table.txt'
    flow_log_file = 'Test_Files/flow_logs.txt'   
    
    lookup_dict = load_lookup_table(lookup_file)
    tag_count, port_protocol_count = process_flow_logs(flow_log_file, lookup_dict)
    
    generate_output_files(tag_count, port_protocol_count)
    print("Output files generated - tag_count.csv, port_protocol_count.csv")

if __name__ == "__main__":
    main()
