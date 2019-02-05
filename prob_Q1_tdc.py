import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from sklearn import linear_model
from scipy import stats
import datetime
plt.style.use('ggplot')

data=pd.read_csv("Incidents_Responded_to_by_Fire_Companies.csv")
print(len(data))

#### Part 1
most_common_incident=data['INCIDENT_TYPE_DESC'].value_counts().max()
fraction_mostcommonincident=most_common_incident/len(data)
print(fraction_mostcommonincident)

#### Part 2
#Staten Island false call rate
statenisland_df=data[data['BOROUGH_DESC'].str.contains('Staten')]
staten_falsecalls=(len(statenisland_df[statenisland_df['INCIDENT_TYPE_DESC'].str.contains('710 - Malicious, mischievous false call, other')]))
staten_total=(len(statenisland_df))
staten_falsecall_rate=staten_falsecalls/staten_total

#Manhattan false call rate
manhattan_df=data[data['BOROUGH_DESC'].str.contains('Manhattan')]
manhattan_falsecalls=(len(manhattan_df[manhattan_df['INCIDENT_TYPE_DESC'].str.contains('710 - Malicious, mischievous false call, other')]))
manhattan_total=(len(manhattan_df))
manhattan_falsecall_rate=manhattan_falsecalls/manhattan_total

print(staten_falsecall_rate/manhattan_falsecall_rate)

#### Part 3

#convert incident date-time to datetime format as a new column
data['formatted_incident_time']=pd.to_datetime(data['INCIDENT_DATE_TIME'])

#add new column for just hour
data['incident_hour']=data['formatted_incident_time'].dt.hour

cookingfire_df=data[data['INCIDENT_TYPE_DESC'].str.contains('113 - Cooking fire, confined to container',case=False)==True]
cookingfire_df.head()

total_incident_hourly_list=np.array(data['incident_hour'].value_counts())
cooking_incident_hourly_list=np.array(cookingfire_df['incident_hour'].value_counts())
ratio=(cooking_incident_hourly_list/total_incident_hourly_list)

#lets find the proportion of total incidents which were cooking fire related
max_proportion=max(ratio)
hour_of_day_with_max_cooking=list(ratio).index(max_proportion)
print(max_proportion,hour_of_day_with_max_cooking)
#probably fell asleep

cooking_incident_hourly_list=np.array(cookingfire_df['incident_hour'].value_counts())

#### Part 5

#make smaller dataframe with only the relevant columns
COdetector_data=data[['INCIDENT_TYPE_DESC','TOTAL_INCIDENT_DURATION','CO_DETECTOR_PRESENT_DESC']]
COdetector_data.dropna(inplace=True)
COdetector_data['CO_DETECTOR_PRESENT_DESC'].value_counts()

#more events when CO detector is present comapred to absent
CO_present_df=COdetector_data[COdetector_data['CO_DETECTOR_PRESENT_DESC']=='Yes']
CO_absent_df=COdetector_data[COdetector_data['CO_DETECTOR_PRESENT_DESC']=='No']
print(len(CO_present_df),len(CO_absent_df),len(COdetector_data))

bins = [20, 30, 40, 50, 60,70]
CO_present_bins = CO_present_df.groupby([pd.cut(CO_present_df.TOTAL_INCIDENT_DURATION/60, bins, right=True, include_lowest=True)])
CO_absent_bins = CO_absent_df.groupby([pd.cut(CO_absent_df.TOTAL_INCIDENT_DURATION/60, bins, right=True, include_lowest=True)])
print("CO present durations (minutes)",CO_present_bins.size())
print("CO absent durations (minutes)",CO_absent_bins.size())

#we have to normalize the frequency to total incidents with and withough CO detector to enable a comparison
CO_present_freq=np.array(CO_present_bins.size()[:])/len(CO_present_df)
CO_absent_freq=np.array(CO_absent_bins.size()[:])/len(CO_absent_df)
print(CO_present_freq)
print(CO_absent_freq)
print('ratio of the ''CO detector absent'' frequency to the ''CO detector present'' frequency: ',CO_absent_freq/CO_present_freq)

#incidents are longer when CO is present compared to when CO is absent
X=np.array([25,35,45,55,65])
y=CO_absent_freq/CO_present_freq
plt.plot(X,y,'x')
plt.show()

X=X.reshape(-1, 1)
reg = linear_model.LinearRegression().fit(X, y)
print(reg.score(X, y),reg.intercept_) 
reg.predict(np.array([[39]]))

#### Part 6

buildingfire_df=data[data['INCIDENT_TYPE_DESC'].str.contains('111 - Building fire')]
smokescare_df=data[data['INCIDENT_TYPE_DESC'].str.contains('651 - Smoke scare')]

bldgfire_units=buildingfire_df['UNITS_ONSCENE'].mean()
smokescare_units=smokescare_df['UNITS_ONSCENE'].mean()

print(bldgfire_units/smokescare_units)

#### Part 7

buildingfire_df['formatted_arrival_time']=pd.to_datetime(buildingfire_df['ARRIVAL_DATE_TIME'])
buildingfire_df['formatted_incident_time']=pd.to_datetime(buildingfire_df['INCIDENT_DATE_TIME'])

buildingfire_df['time_to_arrive']=buildingfire_df['formatted_arrival_time']-buildingfire_df['formatted_incident_time']

buildingfire_df['time_to_arrive']=buildingfire_df['time_to_arrive'].dt.total_seconds()
buildingfire_df.head()

third_quartile=buildingfire_df['time_to_arrive'].quantile(.75)#, axis=0, numeric_only=False, interpolation='linear')
print(third_quartile)

#### Part 8

census_data=pd.read_csv('2010+Census+Population+By+Zipcode+(ZCTA).csv')
census_data.set_index('Zip Code ZCTA',inplace=True)
census_data.head()

buildingfire_df['ZIP_CODE']=pd.to_numeric(buildingfire_df['ZIP_CODE'],downcast='integer')
zipcode_incidents=pd.DataFrame(buildingfire_df['ZIP_CODE'].value_counts())
zipcode_incidents.rename(columns={'ZIP_CODE':'no_incidents'},inplace=True)
zipcode_incidents.head()

#join both tables using zipcode as index
zipcode_incidents=zipcode_incidents.join(census_data,how='inner')
zipcode_incidents.head()
plt.scatter(zipcode_incidents['2010 Census Population'],zipcode_incidents['no_incidents'])
plt.show()

slope, intercept, r_value, p_value, std_err = stats.linregress( zipcode_incidents['2010 Census Population'],zipcode_incidents['no_incidents'])
print(r_value)

#### Part 9
CO_all_list=COdetector_data['TOTAL_INCIDENT_DURATION'].tolist()
CO_all_list=np.array(CO_all_list)/60
CO_present=COdetector_data[COdetector_data['CO_DETECTOR_PRESENT_DESC']=='Yes']['TOTAL_INCIDENT_DURATION']
CO_present=CO_present/60
CO_present_longer_than_60min_freq=len(CO_present[CO_present>60.0])/len(CO_present)
CO_long=(np.sum(CO_present_longer_than_60min_freq))

CO_present_shorter_than_60min_freq=len(CO_present[CO_present<=60.0])/len(CO_present)
CO_short=(np.sum(CO_present_shorter_than_60min_freq))

CO_absent=COdetector_data[COdetector_data['CO_DETECTOR_PRESENT_DESC']=='No']['TOTAL_INCIDENT_DURATION']
CO_absent=CO_absent/60
CO_absent_longer_than_60min_freq=len(CO_absent[CO_absent>60.0])/len(CO_absent)
CO_absent_shorter_than_60min_freq=len(CO_absent[CO_absent<=60.0])/len(CO_absent)
noCO_long=(np.sum(CO_absent_longer_than_60min_freq))
noCO_short=(np.sum(CO_absent_shorter_than_60min_freq))

obs = np.array([[CO_long, CO_short], [noCO_long, noCO_short]])
chi2, p, dof, expected = stats.chi2_contingency(obs)
print (chi2,p)
