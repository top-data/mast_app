
import sys

from ai_functions import return_ai_output

input_file_name = 'YAR000H.csv' #sys.argv[1]

ai_output = return_ai_output(input_file_name)
ai_output.to_json(f"{input_file_name}_output.csv")
ai_output.to_csv(f"{input_file_name}_output.csv", index=False)

# return_ai_output("2K0084M_mast_model_data.csv")
