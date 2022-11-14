import csv

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
        'Company Name': parse_company_name(data),
        'Company Domain Name': parse_company_name(data),
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


if __name__ == "__main__":
    companies = []
    with open('data/FullTeamData.csv', newline='',encoding='utf8') as data_csvfile:
        reader = csv.DictReader(data_csvfile)
        for row in reader:
            companies.append(parse_company_record(row))
    with open('data/company_import_file.csv', 'w', newline='', encoding='utf8') as company_csvfile:
        fieldnames = companies[0].keys()
        writer = csv.DictWriter(company_csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for company in companies:
            writer.writerow(company)