
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. تحميل البيانات (Data Ingestion)
# سنستخدم بيانات محدثة من مستودع موثوق
url = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
df = pd.read_csv(url)

# 2. تنظيف وتجهيز البيانات (Data Preprocessing)
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# إضافة عمود لحساب الحالات النشطة (تقديرياً)
df['Active'] = df['Confirmed'] - df['Recovered'] - df['Deaths']

# استخراج آخر تحديث للبيانات للتقارير الثابتة
latest_date = df['Date'].max()
df_latest = df[df['Date'] == latest_date].sort_values(by='Confirmed', ascending=False)

print(f"تم تحميل البيانات بنجاح. آخر تحديث: {latest_date.date()}")

# --- مرحلة التمثيل المرئي (Visualization) ---

# أولاً: خريطة العالم التفاعلية (Choropleth Map)
fig_map = px.choropleth(
    df_latest, 
    locations="Country",
    locationmode='country names',
    color="Confirmed",
    hover_name="Country",
    hover_data=["Deaths", "Recovered"],
    title=f"الانتشار العالمي لفيروس كورونا - تحديث {latest_date.date()}",
    color_continuous_scale="Reds"
)

# ثانياً: تحليل الاتجاه الزمني العالمي (Global Timeline)
df_global_daily = df.groupby('Date')[['Confirmed', 'Deaths', 'Recovered']].sum().reset_index()
fig_line = px.line(
    df_global_daily, 
    x="Date", 
    y=["Confirmed", "Deaths"],
    title="تطور الإصابات والوفيات عالمياً مع مرور الوقت",
    labels={"value": "عدد الحالات", "variable": "التصنيف"},
    color_discrete_map={"Confirmed": "blue", "Deaths": "red"}
)

# ثالثاً: مقارنة أعلى 10 دول متضررة (Top 10 Countries)
top_10 = df_latest.head(10)
fig_bar = px.bar(
    top_10,
    x='Country',
    y='Confirmed',
    text='Confirmed',
    title="أعلى 10 دول من حيث عدد الإصابات المؤكدة",
    color='Confirmed',
    color_continuous_scale='Viridis'
)
fig_bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')

# رابعاً: تحليل نسبة الوفيات (Mortality Rate)
df_latest['Mortality Rate (%)'] = (df_latest['Deaths'] / df_latest['Confirmed']) * 100
fig_mortality = px.scatter(
    df_latest.head(20),
    x="Confirmed",
    y="Mortality Rate (%)",
    size="Deaths",
    color="Country",
    hover_name="Country",
    title="العلاقة بين عدد الإصابات ونسبة الوفيات (أول 20 دولة)",
    size_max=60
)

# --- عرض النتائج ---
# يمكنك تشغيل كل شكل على حدة
fig_map.show()
fig_line.show()
fig_bar.show()
fig_mortality.show()











