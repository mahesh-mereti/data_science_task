

import code
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import matplotlib.pyplot as plt
import seaborn as sns
import random
from IPython import get_ipython


credentials = service_account.Credentials.from_service_account_file(
    "/mnt/c/users/Mahesh M/key/key.json", scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

bqclient = bigquery.Client(credentials=credentials, project=credentials.project_id,)
name_group_query = """
    select 
unit,
timee,
sum(cum_tests_orig) as cum_tests_orig,
sum(new_tests_orig) as new_tests_orig,
sum(new_cases_orig) as new_cases_orig,
sum(new_deaths_orig) as new_deaths_orig
 from (
select 
 unit,
 CASE WHEN cum_tests_orig ='NA' THEN 0
ELSE CAST(cum_tests_orig AS INT64)
END AS cum_tests_orig ,

 CASE WHEN new_tests_orig ='NA' THEN 0
ELSE CAST(new_tests_orig AS INT64)
END AS new_tests_orig ,

 CASE WHEN new_cases_orig ='NA' THEN 0
ELSE CAST(new_cases_orig AS INT64)
END AS new_cases_orig ,

 CASE WHEN new_deaths_orig ='NA' THEN 0
ELSE CAST(new_deaths_orig AS INT64)
END AS new_deaths_orig ,
substr(cast(timee as string),1,7) as timee
  FROM `sample-project-8884.trang_ng.find_cov_track_data` where sett = 'country' 
) a 
group by unit,timee 

"""


query_results = bqclient.query(name_group_query)
df = bqclient.query(name_group_query).to_dataframe()

#print(df.head())
df = pd.DataFrame(df.head(8))
#print(df.head())
#df.boxplot(grid='false', color='blue',fontsize=10, rot=30 )
df.boxplot(by ='timee',grid='True',column =['cum_tests_orig'], color='red')
plt.show()





# for result in query_results:
#     print(str(result[0]),"        ",str(result[1]),"        ",str(result[2]),"        ",str(result[3]))

# print(df.shape)
# print(df.head())
#print(df.columns)
# print(df.dtypes)
# print(df.nunique(axis=0))
# df.boxplot(df.head())
# df.boxplot(by ='unit', column =['new_tests_orig'], grid = True)
# plt.show()


# sns.lmplot('new_tests_orig', 'new_tests_orig', data=df, fit_reg=False)
# sns.kdeplot(df.new_tests_orig, df.new_tests_orig); 
# plt.show()

#
# df = pd.DataFrame()
# df['x'] = random.sample(range(1, 50), 25)
# df['y'] = random.sample(range(1, 100), 25)
# print(); print(df.head())
# print(); print(df.tail())

# sns.lmplot('x', 'y', data=df, fit_reg=False)
# sns.kdeplot(df.y); plt.show()
# sns.kdeplot(df.y, df.x); plt.show()
# sns.distplot(df.x); plt.show()

# plt.hist(df.x, alpha=.3)
# sns.rugplot(df.x)
# plt.show()
