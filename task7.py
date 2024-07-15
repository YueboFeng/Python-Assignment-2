import re

class RegexHandler:
    """ This class is to prescribe the format of emails and phones. """
    def __init__(self) -> None:
        """ This method is to prescribe the format of emails and phones. """
        self.email_regex = r"\b[A-Za-z]+(?:\.[A-Za-z]+)*@[A-Za-z]+\.[A-Za-z]{2,}\b"
        self.phone_regex = r"(?:\((61)\)0|\b61)[0-9]{8,9}"

    def validate_email(self, str2check: str) -> bool:
        """ This method is to judge the validation of emails. """
        if re.match(self.email_regex, str2check):
            return True
        else:
            return False
    
    def validate_phone(self, str2check: str) -> bool:
        """ This method is to judge the validation of phones. """
        if re.match(self.phone_regex, str2check):
            return True
        else:
            return False


def prop_email_matcher(prop_fpath: str, email_fpath: str) -> str:
    """ This method is to merge properties and emails. """
    handler = RegexHandler()
    result = []
    prop_email_dict = {}
    
    with open(prop_fpath, "r") as prop_f, open(email_fpath, "r") as email_f:
        prop_header = prop_f.readline().strip().split(",")
        properties = prop_f.readlines()
        email_header = email_f.readline().strip().split(",")
        emails = email_f.readlines()

        # Locate variables of prop_id, address in properties, and prop_id, email in emails with their headers.
        prop_prop_id_index = prop_header.index("prop_id")
        address_index = prop_header.index("full_address")
        email_prop_id_index = email_header.index("prop_id")
        email_index = email_header.index("email")
        result.append(prop_header[prop_prop_id_index] + "," +
            prop_header[address_index] + "," +
            email_header[email_index])

        # Merge information of properties and emails based on their locations.
        for i in range(len(properties)):
            prop_id = properties[i].strip().split(",")[prop_prop_id_index]
            address = properties[i].strip().split(",")[address_index]
            for email in emails:
                email_prop_id = email.strip().split(",")[email_prop_id_index]
                email = email.strip().split(",")[email_index]
                if email_prop_id == prop_id:
                    if handler.validate_email(email):
                        prop_email_dict[prop_id] = address, email
                    else:
                        prop_email_dict[prop_id] = address, ""

        for prop_id, (address, email) in prop_email_dict.items():
            result.append(f"{prop_id},{address},{email}")
        output = "\n".join(result)
    return output


def prop_phone_matcher(prop_fpath: str, phone_fpath: str) -> str:
    """ This method is to merge properties and phones. """
    handler = RegexHandler()
    result = []
    prop_phone_dict = {}
    
    with open(prop_fpath, "r") as prop_f, open(phone_fpath, "r") as phone_f:
        prop_header = prop_f.readline().strip().split(",")
        properties = prop_f.readlines()
        phone_header = phone_f.readline().strip().split(",")
        phones = phone_f.readlines()

        # Locate variables of prop_id, address in properties, and prop_id, phone in phones with their headers.
        prop_prop_id_index = prop_header.index("prop_id")
        address_index = prop_header.index("full_address")
        phone_prop_id_index = phone_header.index("prop_id")
        phone_index = phone_header.index("phone")
        result.append(prop_header[prop_prop_id_index] + "," +
            prop_header[address_index] + "," +
            phone_header[phone_index])

        # Merge information of properties and phones based on their locations.
        for i in range(len(properties)):
            prop_id = properties[i].strip().split(",")[prop_prop_id_index]
            address = properties[i].strip().split(",")[address_index]
            for phone in phones:
                phone_prop_id = phone.strip().split(",")[phone_prop_id_index]
                phone = phone.strip().split(",")[phone_index]
                if phone_prop_id == prop_id:
                    if handler.validate_phone(phone):
                        prop_phone_dict[prop_id] = address, phone
                    else:
                        prop_phone_dict[prop_id] = address, ""

        for prop_id, (address, phone) in prop_phone_dict.items():
            result.append(f"{prop_id},{address},{phone}")
        output = "\n".join(result)
    return output


def merge_prop_email_phone(prop_fpath: str, email_phone_fpath: str) -> str:
    """ This methos is to merge properties, emails and phones. """
    handler = RegexHandler()
    result = []
    prop_email_phone_dict = {}

    with open(prop_fpath, "r") as prop_f, open(email_phone_fpath, "r") as email_phone_f:
        prop_header = prop_f.readline().strip().split(",")
        properties = prop_f.readlines()

        email_phone_header = email_phone_f.readline().strip().split(",")
        email_phones = email_phone_f.readlines()
        
        # Locate variables of prop_id, address in properties, and prop_id, email, and phone in email_phones with their headers.
        prop_prop_id_index = prop_header.index("prop_id")
        address_index = prop_header.index("full_address")
        email_phone_prop_id_index = email_phone_header.index("prop_id")
        email_index = email_phone_header.index("email")
        phone_index = email_phone_header.index("phone")
        result.append(prop_header[prop_prop_id_index] + "," +
            prop_header[address_index] + "," +
            email_phone_header[email_index] + "," +
            email_phone_header[phone_index])
            
        # Merge information of properties, emails and phones based on their locations.
        for i in range(len(properties)):
            prop_id = properties[i].strip().split(",")[prop_prop_id_index]
            address = properties[i].strip().split(",")[address_index]
            for email_phone in email_phones:
                email_phone_prop_id = email_phone.strip().split(",")[email_phone_prop_id_index]
                email = email_phone.strip().split(",")[email_index]
                phone = email_phone.strip().split(",")[phone_index]
                if prop_id == email_phone_prop_id:
                    if handler.validate_email(email):
                        if handler.validate_phone(phone):
                            prop_email_phone_dict[prop_id] = address, email, phone
                        else:
                            prop_email_phone_dict[prop_id] = address, email, ""
                    else:
                        if handler.validate_phone(phone):
                            prop_email_phone_dict[prop_id] = address, "", phone

        for prop_id, (address, email, phone) in prop_email_phone_dict.items():
            result.append(f"{prop_id},{address},{email},{phone}")
        output = "\n".join(result)
    return output
    

if __name__ == "__main__":
    print("Task 1 results: ")
    print(prop_email_matcher("sample_properties.csv", "sample_properties_email_phone.csv"))
    print("="*50)
    print("Task 2 results: ")
    print(prop_phone_matcher("sample_properties.csv", "sample_properties_email_phone.csv"))
    print("="*50)
    print("Task 3 results: ")
    print(merge_prop_email_phone("sample_properties.csv", "sample_properties_email_phone.csv"))
