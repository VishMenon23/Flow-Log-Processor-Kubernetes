import csv

def create_protocol_dict(csv_filename):
    protocol_dict = {}
    with open(csv_filename, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row['Decimal']
            value = row['Keyword'].lower()
            protocol_dict[key] = value
    return protocol_dict

# Example usage:
csv_filename = 'protocols_code_master.csv'
protocol_dict = create_protocol_dict(csv_filename)

# Print the resulting dictionary
print(protocol_dict)
