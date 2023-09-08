def return_ai_output(csv_file_name):

    import pandas as pd
    import numpy as np
    import joblib
    import warnings
    warnings.filterwarnings('ignore')
    warnings.simplefilter('ignore')

    def prep_train_test(df):

        # dropping some extra columns
        df_prep = df.copy()
        drop_columns = ["Unnamed: 0",'Unnamed: 0.1', "NID", "Herd", "Rx_Month", "Rx_Year", "Prev_AllRxCodes", "RxHShort"]
        df_prep.drop(drop_columns, axis=1, inplace=True, errors='ignore')

        # replacing all missing with nan
        df_prep.replace("None", np.nan, inplace=True)
        df_prep.replace("False", np.nan, inplace=True)
        df_prep.replace("FALSE", np.nan, inplace=True)

        # dropping columns with high missing > 0.3
        # high_missing = df_prep.columns[df_prep.isnull().mean() > 0.3]
        high_missing = ['M_Sys', 'HWI', 'ABV_M_Resist', 'TLSCC', 'TL150SCC', 'TL200SCC',
                        'TL_mean_logSCC', 'TL_sd_logSCC', 'DSLB', 'pre_num_tests_0to30',
                        'pre_num_tests_0to30_max', 'pre_num_tests_0to30_logmean',
                        'pre_num_tests_0to30_SCC>150', 'pre_num_tests_0to30_SCC>200',
                        'pre_num_tests_0to30_SCC>1000', 'pre_num_tests_31to60',
                        'pre_num_tests_31to60_max', 'pre_num_tests_31to60_logmean',
                        'pre_num_tests_31to60_SCC>150', 'pre_num_tests_31to60_SCC>200',
                        'pre_num_tests_31to60_SCC>1000', 'pre_num_tests_61to90',
                        'pre_num_tests_61to90_max', 'pre_num_tests_61to90_logmean',
                        'pre_num_tests_61to90_SCC>150', 'pre_num_tests_61to90_SCC>200',
                        'pre_num_tests_61to90_SCC>1000', 'pre_num_tests_g90',
                        'pre_num_tests_g90_max', 'pre_num_tests_g90_logmean',
                        'pre_num_tests_g90_SCC>150', 'pre_num_tests_g90_SCC>200',
                        'pre_num_tests_g90_SCC>1000']
        df_prep.drop(columns=high_missing, axis=1, errors='ignore', inplace=True)

        high_corr = ['LIFE200SCC',
                    'prelact_SCC_count',
                    'prelact_SCC>150',
                    'prelact_SCC>200',
                    'pre_herd_greater14day_mast_percent',
                    'pre_herd_SCC__DIM_more30_percent_g150',
                    'pre_herd_SCC_percent_g200',
                    'pre_herd_SCC__DIM_less31_percent_g200',
                    'pre_herd_SCC__DIM_more30_percent_g200']

        df_prep.drop(columns=high_corr, axis=1, errors='ignore', inplace=True)
        
        # extracting possible outcomes from data
        possible_outcomes = [col for col in df_prep if col.startswith('Outcome_')] 
        features = df_prep.drop(possible_outcomes, axis=1, errors='ignore')

        # drop Gest
        features.drop("Gest", axis=1, inplace=True, errors='ignore')
        
        # drop quarter
        features.drop("Quarter", axis=1, inplace=True, errors='ignore')
        
        return features 

    outcome_list = ['Outcome_Sold', 'Outcome_Shortloss', 'Outcome_Longloss', 'Outcome_Failure', 'Outcome_Recurred']

    df = pd.read_csv(csv_file_name)
    ai_output = pd.DataFrame([])
    ai_output["CowID"] = df["NID"]
    ai_output['Lact'] = df['Lact']
    features = prep_train_test(df)

    for outcome in outcome_list:
        
        model = joblib.load(f'model_{outcome}_main.joblib')
        proba = model.predict_proba(features)[:,1]
        ai_output[outcome.replace('Outcome_', 'Cow ')] = np.round(proba*100, 0)
        ai_output[outcome.replace('Outcome_', 'Herd ')] = round(ai_output[outcome.replace('Outcome_', 'Cow ')].mean())

    def calculate_class(row):
        if max(row['Cow Shortloss'], row['Cow Longloss'], row['Cow Sold']) > 90:
            return 5 #"5.Cull-High"
        elif max(row['Cow Sold'], row['Cow Shortloss'], row['Cow Longloss'], row['Cow Recurred']) > 70:
            return 4 # "4.Cull-Mod"
        elif max(row['Cow Sold'], row['Cow Shortloss'], row['Cow Longloss'], row['Cow Recurred']) < 30:
            return 1 #"1.Sample-High"
        elif max(row['Cow Sold'], row['Cow Shortloss'], row['Cow Longloss'], row['Cow Recurred']) < 50:
            return 2 # "2.Sample-Mod"
        else:
            return 3 # "3.Sample-Low"

    ai_output['Cow Quality'] = ai_output.apply(calculate_class, axis=1)

    return ai_output



        