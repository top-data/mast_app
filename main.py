
import sys

from ai_functions import return_ai_output

input_file_name = sys.argv[1]

ai_output = return_ai_output(input_file_name)
ai_output.to_json("ai_output.json")
ai_output.to_csv("ai_output.csv", index=False)

# return_ai_output("2K0084M_mast_model_data.csv")
