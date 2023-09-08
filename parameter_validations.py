import re

#get_validation
class Extracted_Data_Validations:
    def __init__(self, data):
        self.data = data

    gst_location_list = []
    gst_data = {
                    "VALID":[],
                    "INVALID":[],
            }
    Consignee_details = {

    }
    Consignor_details = {

    }
    def gst_validation(self):

        partial_pattern = r'\b[A-Z0-9]{15}\b'
        # Find all possible GSTINs in the text
        partial_gst_numbers = re.findall(partial_pattern, self.data)

        exact_pattern = r'\b[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9]{1}[A-Z]{1}[A-Z0-9]{1}\b'
        # Find all exact GSTINs in the text
        gst_numbers = re.findall(exact_pattern, self.data)
        print(partial_gst_numbers)


        new_numbers_to_verify = []
        for num1 in gst_numbers:
            for num2 in partial_gst_numbers:
                if num1 == num2:
                    Extracted_Data_Validations.gst_data["VALID"].append(num2)
                    Extracted_Data_Validations.gst_location_list.append(num2)
                else:
                    new_numbers_to_verify.append(num2)

        print(f"verfying {new_numbers_to_verify}")


        for gst_number_to_verify in new_numbers_to_verify:
            possible_gst_index = self.data.index(gst_number_to_verify)

            if 'GST' in self.data[possible_gst_index-20:possible_gst_index+len(gst_number_to_verify)] or 'gst' in data[possible_gst_index-20:possible_gst_index+len(gst_number_to_verify)]:
                Extracted_Data_Validations.gst_data["INVALID"].append(gst_number_to_verify)
                Extracted_Data_Validations.gst_location_list.append(possible_gst_index)
                print(f"Incorrect GST Number {gst_number_to_verify}")
            else:
                print(f"{gst_number_to_verify} is not a GST Number")

        return Extracted_Data_Validations.gst_data

    def Identity_Segregation(self):

        L_and_T_Possible_names = ["L&T", "Larsen", "Turbo", "L & T"]
        l_and_t_gst_file = open('l&T_GST_LIST.txt', 'r')
        l_and_t_gst_data = [line.split(',') for line in l_and_t_gst_file.readlines()]
        for extracted_gst in Extracted_Data_Validations.gst_data["VALID"]:
            for gst_number_data in l_and_t_gst_data:
                if extracted_gst == gst_number_data[0] and len(Extracted_Data_Validations.gst_data.values()) == 2:
                    print(f"{extracted_gst} belongs to L&T {gst_number_data[2]} in {extracted_gst[1]} state")
                    Extracted_Data_Validations.Consignee_details["GSTN"] = gst_number_data[0]
                    Extracted_Data_Validations.Consignee_details["status"] = gst_number_data[1]
                    Extracted_Data_Validations.Consignee_details["State"] = gst_number_data[2]
            else:
                print(f"{extracted_gst} belongs to consignor")
                Extracted_Data_Validations.Consignor_details["GSTN"] = extracted_gst
                Extracted_Data_Validations.Consignor_details["GSTN_STATUS"] = "VALID"


        if "GSTN" not in Extracted_Data_Validations.Consignee_details and "GSTN" in Extracted_Data_Validations.Consignor_details:
            for extracted_gst in Extracted_Data_Validations.gst_data["INVALID"]:
                Extracted_Data_Validations.Consignee_details["GSTN"] = extracted_gst
                Extracted_Data_Validations.Consignee_details["GSTN_STATUS"] = "INVALID"
                gst_number_index = self.data.index(extracted_gst)
                print("invalid GSTN Location ", gst_number_index)



        segragated_data = {
            "CONSIGNEE": Extracted_Data_Validations.Consignee_details,
            "CONSIGNOR": Extracted_Data_Validations.Consignor_details
        }
        return segragated_data
















    #
    #         elif 'O' in num2 or '0' in num2:
    #             num2 = num2[:2].replace('O', '0')+ num2[2:7].replace('0', 'O')+num2[7:11].replace('O', '0')+num2[11].replace('0', 'O')+num2[12].replace('O', '0')+num2[13].replace('0', 'O')
    #             # num2 = re.findall(pattern, num2)
    #             print("num2", num2)







    # return gst_number_list


# gst_validation(' 27AAACLOL40PEZ6 77AALFJ3318B1Z5')

# print(res)
#po

#state_code

#consignee identifier
