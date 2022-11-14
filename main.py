import csv
from itertools import islice

def parse_company_name(data):
    result = ""
    if data["Program"]:
        result = f'{data["Program"]}#{data["Team Number"]}'
    return result

def parse_first_name(data, target):
    name_data = data[target].split(" ")
    if len(name_data) > 0:
        return name_data[0]
    return ""

def parse_last_name(data, target):
    name_data = data[target].split(" ")
    if len(name_data) > 1:
        return ' '.join(name_data[1:])
    return ""

def parse_deal_name(data):
    result = ""
    if data["Most Recent Season Secured"]:
        result = f'{data["Most Recent Season Secured"]} Season'
    return result

def generate_deal_stage(data):
    result = ""
    if data["Most Recent Season Secured"]:
        result = "Appointment Scheduled"
    return result

def generate_deal_pipeline(data):
    result = ""
    if data["Most Recent Season Secured"]:
        result = "Sales Pipeline"
    return result

def parse_company_record(data):
    """
    Parses a single company record from raw data
    """
    record = {
        'Company Domain': f'{data["Program"]}{data["Team Number"]}.org',
        'Company Name': parse_company_name(data),
        'City': data["Team City"],
        'State': data["Team State Province"],
        'Postal Code': data["Team Postal Code"],
        'Description': f'{data["Program"]} team #{data["Team Number"]}, {data["Team Nickname"]}',
        'Number of Employees': data["Youth Team Members Count"],
        'Website URL': f'https://{data["Program"].lower()}-events.firstinspires.org/team/{data["Team Number"]}',
        'Year Founded': data["Team Rookie Year"],
        'Type': 'Team',
        'Program': data["Program"]

    }
    return record



def parse_company_contact_records(data, name_key, email_key, phone_key):
    """
    Parses contact records for the LC1, LC2, and Team Admin in the record.
    """
    record = {
        'First Name': parse_first_name(data, name_key),
        'Last Name': parse_last_name(data, name_key),
        'Email': data[email_key],
        'Phone': data[phone_key],
        'Company Name': parse_company_name(data),
        'Type': 'Team Contact'
    }
    return record


if __name__ == "__main__":
    companies = []
    contacts = []
    keys_list = [
        ['LC1 Name', 'LC1 Email', 'LC1 Phone'],
        ['LC2 Name', 'LC2 Email', 'LC2 Phone'],
        ['Team Admin Name', 'Team Admin Email', 'Team Admin Phone']
    ]
    with open('data/FullTeamData.csv', newline='',encoding='utf8') as data_csvfile:
        reader = csv.DictReader(data_csvfile)
        for row in islice(reader,10):
            companies.append(parse_company_record(row))
            for key_list in keys_list:
                if row[key_list[0]]:
                    contacts.append(parse_company_contact_records(row, key_list[0], key_list[1], key_list[2]))

    with open('data/company_import_file.csv', 'w', newline='', encoding='utf8') as company_csvfile:
        fieldnames = companies[0].keys()
        writer = csv.DictWriter(company_csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for company in companies:
            writer.writerow(company)

    with open('data/contact_import_file.csv', 'w', newline='', encoding='utf8') as contact_csvfile:
        fieldnames = contacts[0].keys()
        writer = csv.DictWriter(contact_csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for contact in contacts:
            writer.writerow(contact)


