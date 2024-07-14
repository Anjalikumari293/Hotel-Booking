#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# # Loading the Dataset

# In[2]:


df = pd.read_csv('Hotel_Booking_DataSet.csv')


# # Exploratory Data Analysis and Data Cleaning

# In[3]:


df.head()


# In[4]:


df.tail()


# In[5]:


df=df.drop(['name','email','phone-number','credit_card'], axis = 1)


# In[6]:


df.shape


# In[7]:


df.columns


# In[8]:


df.info()


# In[9]:


df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])


# In[10]:


df.info()


# In[11]:


df.describe(include = object)


# In[12]:


for col in df.describe(include = object).columns:
    print(col)
    print(df[col].unique())
    print('-'*50)


# In[13]:


df.isnull().sum()


# In[14]:


df.drop(['company','agent'],axis = 1, inplace = True)


# In[15]:


df.dropna(inplace = True)


# In[16]:


df.isnull().sum()


# In[17]:


df = df[df['adr']< 5000]


# In[18]:


df.describe()


# # Data Analysis And Visaualization

# In[19]:


cancelled_perc = df['is_canceled'].value_counts(normalize = True)


# In[20]:


print(cancelled_perc)

plt.figure()
plt.title('Reservation status count')
plt.bar(['Not canceled','Canceled'],df['is_canceled'].value_counts())
plt.savefig('Fig1')
plt.show()


# In[21]:


plt.figure()
ax1 = sns.countplot(x = 'hotel', hue = 'is_canceled', data = df, palette = 'Blues')
legend_labels,_=ax1. get_legend_handles_labels()
ax1.legend(bbox_to_anchor = (1,1))
plt.title('Reservation status in different Hotels', size = 20)
plt.xlabel('Hotel')
plt.ylabel('Number Of Reservation')
plt.legend(['Not canceled','Canceled'])
plt.savefig('Fig2')
plt.show()


# In[22]:


resort_hotel = df[df['hotel'] == 'Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize = True)


# In[23]:


city_hotel = df[df['hotel'] == 'City Hotel']
city_hotel['is_canceled'].value_counts(normalize = True)


# In[24]:


resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[25]:


plt.figure(figsize=(15,8))
plt.title('Average Daily Rate in City and Resort Hotel', fontsize = 20)
plt.plot(resort_hotel.index,resort_hotel['adr'],label='Resort Hotel')
plt.plot(city_hotel.index,city_hotel['adr'],label='City Hotel')
plt.legend()
plt.savefig('Fig3')
plt.show()


# In[26]:


df['month'] = df['reservation_status_date'].dt.month
plt.figure(figsize=(16,8))
ax1 = sns.countplot(x = 'month', hue = 'is_canceled',data= df, palette='bright')
legend_labels,_=ax1. get_legend_handles_labels()
ax1.legend(bbox_to_anchor = (1,1))
plt.title('Reservation status per Month', size = 20)
plt.xlabel('month')
plt.ylabel('Number Of Reservation')
plt.legend(['Not canceled','Canceled'])
plt.savefig('Fig4')
plt.show()


# In[27]:


plt.figure(figsize = (15,8))
plt.title('ADR per month', fontsize = 20)
#sns.barplot('month','adr', data = df[df['is_canceled'] == 1].groupby('month')[['adr']].sum().reset_index())
# Group, aggregate, and reset index (already done in your code)
adr_by_month = df[df['is_canceled'] == 1].groupby('month')[['adr']].sum().reset_index()

# Use the new DataFrame in barplot
sns.barplot(x='month', y='adr', data=adr_by_month, palette="plasma")
plt.savefig('Fig5')
plt.show()


# In[28]:


cancelled_data = df[df['is_canceled']==1]
top_10_country = cancelled_data['country'].value_counts()[:10]
plt.figure(figsize = (8,8))
plt.title('Top 10 Countries with Reservation Cancelled')
plt.pie(top_10_country, autopct = '%.2f', labels = top_10_country.index)
plt.savefig('Fig6')
plt.show()


# In[29]:


df['market_segment'].value_counts()


# In[30]:


df['market_segment'].value_counts(normalize = True)


# In[31]:


cancelled_data['market_segment'].value_counts(normalize = True)


# In[32]:


import pandas as pd
import matplotlib.pyplot as plt

# Assuming you have your reservation data in a DataFrame named 'df'
cancelled_df = df[df['is_canceled'] == 1]  # Filter for cancelled reservations (defined here)
not_cancelled_df = df[df['is_canceled'] == 0]  # Filter for non-cancelled reservations

# Calculate average daily rate (ADR) for each group
cancelled_df_adr = cancelled_df.groupby('reservation_status_date')[['adr']].mean()
cancelled_df_adr.reset_index(inplace=True)
cancelled_df_adr.sort_values('reservation_status_date', inplace=True)

not_cancelled_df_adr = not_cancelled_df.groupby('reservation_status_date')[['adr']].mean()
not_cancelled_df_adr.reset_index(inplace=True)
not_cancelled_df_adr.sort_values('reservation_status_date', inplace=True)

# Create time series plot
plt.figure(figsize=(20, 6))
plt.title('Average Daily Rate (Cancelled vs. Non-Cancelled)', fontsize = 15)
plt.plot(cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'], label='Cancelled')
plt.plot(not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'], label='Not Cancelled')
plt.legend(fontsize = 20)
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.xlabel('Reservation Status Date')
plt.ylabel('Average Daily Rate')
plt.grid(True)
plt.tight_layout()  # Adjust spacing for readability
plt.savefig('Fig7')
plt.show()


# In[33]:


cancelled_df_adr = cancelled_df_adr[(cancelled_df_adr['reservation_status_date']>'2016') & (cancelled_df_adr['reservation_status_date']<'2017-09')]
not_cancelled_df_adr = not_cancelled_df_adr[(not_cancelled_df_adr['reservation_status_date']>'2016') & (not_cancelled_df_adr['reservation_status_date']<'2017-09')]


# In[34]:


plt.figure(figsize = (20,6))
plt.plot(cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'], label='Cancelled')
plt.plot(not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'], label='Not Cancelled')
plt.legend(fontsize = 20)
plt.title('Average Daily Rate (2016-jan to 2017-sep)',fontsize = 20)
plt.xlabel('Reservation Status Date',fontsize = 15)
plt.ylabel('Average Daily Rate',fontsize = 15)
plt.grid(True)
plt.savefig('Fig8')
plt.show()


# # Analysis By Anjali Kumari

# # Thank You !
