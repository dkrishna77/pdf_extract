import re
# from update_excel_sheet import workbook, worksheet

#get_validation
class Extracted_Data_Validations:

    #Intialization
    def __init__(self, data):
        self.data = data

    gst_location_list = []
    rough_data_for_validation = {
        "CONSIGNEE":{},
        "CONSIGNOR":{}
    }

    Consignee_details = {

    }
    Consignor_details = {

    }


    #gst_validation
    def gst_validation(self):
        #possibility and data correction
        partial_pattern = r'\b[A-Z0-9]{15}\b'
        partial_gst_possibilities = re.findall(partial_pattern, self.data)
        corrected_partial_possibilities = []
        for fetched_data in partial_gst_possibilities:
            corrected_pattern = ''
            corrected_pattern+=fetched_data[:2].replace('O', '0')
            corrected_pattern+=fetched_data[2:7].replace('0', 'O')
            corrected_pattern+=fetched_data[7:11].replace('O', '0')
            corrected_pattern+=fetched_data[11].replace('0', '0')
            corrected_pattern+=fetched_data[12].replace('O', '0')
            corrected_pattern+=fetched_data[13]
            corrected_pattern+=fetched_data[14]

            corrected_partial_possibilities.append(corrected_pattern)


        #exact
        exact_pattern = r'\b[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9]{1}[A-Z]{1}[A-Z0-9]{1}\b'
        Extracted_Data_Validations.gst_numbers = list(set(re.findall(exact_pattern, " ".join(corrected_partial_possibilities))))

        return Extracted_Data_Validations.gst_numbers


    def Gst_Segragation(self):
        l_and_t_gst_file = open('../l&T_GST_LIST.txt', 'r')
        l_and_t_gst_data = l_and_t_gst_file
        l_and_t_gst_gst = [line.split(',')[0] for line in l_and_t_gst_data]

        #GST Segregation
        for extracted_gst in Extracted_Data_Validations.gst_numbers:
            if extracted_gst in l_and_t_gst_gst:
                print(f"{extracted_gst} belongs to L&T Itself")
                Extracted_Data_Validations.Consignee_details["GSTN"] = extracted_gst
                Extracted_Data_Validations.rough_data_for_validation["CONSIGNEE"]["POSSIBLE_STATE_CODE"] = extracted_gst[:2]


            else:
                print(f"{extracted_gst} belongs to consignor")
                Extracted_Data_Validations.Consignor_details["GSTN"] = extracted_gst
                Extracted_Data_Validations.rough_data_for_validation["CONSIGNOR"]["POSSIBLE_STATE_CODE"] = extracted_gst[:2]


        segragated_data = {
            "CONSIGNEE": Extracted_Data_Validations.Consignee_details,
            "CONSIGNOR": Extracted_Data_Validations.Consignor_details
        }
        return segragated_data

    def State_Segragation(self):
        State_file = open("../state_codes.txt")
        State_data = State_file.readlines()
        State_Names = {state.split(',')[1][:2]:state.split(',')[0].capitalize() for state in State_data}

        state_list = []
        for state_code,state_name in State_Names.items():
            if state_name in self.data or state_name in self.data.capitalize():
                state_list.append((state_name,state_code, self.data.index(state_name)))

        # L_and_T_Possible_names = ["L&T", "Larsen", "Turbo", "L & T"]
        fetched_state_names = [state_data[0] for state_data in state_list]
        fetched_state_codes = [state_data[1] for state_data in state_list]
        state_index_locations = [state_data[2] for state_data in state_list]

        if len(state_list) != 0:
            states_fetched = len(state_code)
            for state_code_index,state_code in enumerate(fetched_state_codes):
                if "GSTN" in Extracted_Data_Validations.Consignee_details:
                    if state_code == Extracted_Data_Validations.Consignee_details["GSTN"][:2]:

                        Extracted_Data_Validations.Consignee_details["STATE"] = fetched_state_names[state_code_index]
                        Extracted_Data_Validations.Consignee_details["STATE_CODE"] = state_code
                        # worksheet[f"I{self.row_number}"] = fetched_state_names[state_code_index]
                        # worksheet[f"J{self.row_number}"] = state_code
                        # workbook.save("source.xlsx")

                        fetched_state_names = [state_data[0] for state_data in state_list if state_data[0] != fetched_state_names[state_code_index]]
                        fetched_state_codes = [state_data[1] for state_data in state_list if state_data[1] != state_code]
                        states_fetched -= 1

                if "GSTN" in Extracted_Data_Validations.Consignor_details:
                    if state_code == Extracted_Data_Validations.Consignor_details["GSTN"][:2]:
                        Extracted_Data_Validations.Consignor_details["STATE"] = fetched_state_names[state_code_index]
                        Extracted_Data_Validations.Consignor_details["STATE_CODE"] = state_code
                        # worksheet[f"G{self.row_number}"] = fetched_state_names[state_code_index]
                        # worksheet[f"H{self.row_number}"] = state_code
                        # workbook.save("source.xlsx")



                        fetched_state_names = [state_data[0] for state_data in state_list if state_data[0] != fetched_state_names[state_code_index]]
                        fetched_state_codes = [state_data[1] for state_data in state_list if state_data[1] != state_code]

                        states_fetched-=1


            # print(states_fetched, fetched_state_names, fetched_state_codes)
                if len(fetched_state_names) == 1:
                    if "STATE" not in Extracted_Data_Validations.Consignee_details:
                        Extracted_Data_Validations.Consignee_details["STATE"] = fetched_state_names[0]
                        Extracted_Data_Validations.Consignee_details["STATE_CODE"] = fetched_state_codes[0]
                        # worksheet[f"I{self.row_number}"] = fetched_state_names[state_code_index]
                        # worksheet[f"J{self.row_number}"] = state_code
                        # workbook.save("source.xlsx")



                    elif "STATE" not in Extracted_Data_Validations.Consignor_details:
                        Extracted_Data_Validations.Consignor_details["STATE"] = fetched_state_names[0]
                        Extracted_Data_Validations.Consignor_details["STATE_CODE"] = fetched_state_codes[0]
                        # worksheet[f"G{self.row_number}"] = fetched_state_names[state_code_index]
                        # worksheet[f"H{self.row_number}"] = state_code
                        # workbook.save("source.xlsx")

        if "GSTN" in Extracted_Data_Validations.Consignee_details and Extracted_Data_Validations.Consignee_details["GSTN"] == "97AAACL0140P1ZC" and "STATE" not in Extracted_Data_Validations.Consignee_details:
            Extracted_Data_Validations.Consignee_details["STATE"] = "Other Territory"
            Extracted_Data_Validations.Consignee_details["STATE_CODE"] = 97
            # workbook.save("source.xlsx")



        return {"CONSIGNEE":Extracted_Data_Validations.Consignee_details,"CONSIGNOR":Extracted_Data_Validations.Consignor_details}

    def PO_Number_Identifier(self):
        if 'OGSP' in self.data and 'RR' in self.data:
            start_index = self.data.index(r'OGSP/')
            fetched_po_number = self.data[start_index:start_index+19]
            print("PO_Number", fetched_po_number)
            Extracted_Data_Validations.Consignor_details["PO_NUMBER"] = fetched_po_number
        else:
            print("No PO Number Found...")

        return Extracted_Data_Validations.Consignor_details

    def Inv_Num_Identifier(self):
        inv_indexes = []
        inv_number_flags = ["INV. NUMBER","INV NO.", "INVOICE NUMBER", "INVOICE NO.", "INV. NO.", "INV NO", "INV", "INVOICE"]
        start_index = 0
        captured_data = set()
        for inv_flag in inv_number_flags:
            print("Inovice flag availabe")
            if inv_flag in self.data.upper():
                data_to_check = self.data.upper()
                while True:
                    index = data_to_check.find(inv_flag, start_index)
                    if index == -1:
                        break

                    inv_indexes.append(index)
                    start_index = index + 1
        split_pattern = r'[ \n\\.,]'
        for inv_index in inv_indexes:
            if r"/" in self.data[inv_index:inv_index+16+11]:
                inv_number_possibilities = re.split(split_pattern,self.data[inv_index:inv_index+len(inv_flag)+16+11])
                for ele in inv_number_possibilities:
                    if r'/' in ele and len(ele)>3:
                        captured_data.add(ele)
        if len(captured_data) == 1:
            Extracted_Data_Validations.Consignor_details["INVOICE_NUMBER"] = list(captured_data)[0]
        elif len(captured_data) > 1:
            Extracted_Data_Validations.Consignor_details["REST_DATA"] = captured_data

        return Extracted_Data_Validations.Consignor_details

    def Truck_Number_validation(self):
        pass






