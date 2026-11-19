import pandas as pd

df = pd.read_excel(r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\5.배출구_가동시간(26년_9월_최종양식완료).xlsx", header=1)
print("Columns with header=1:", df.columns)
print("First 5 rows:")
print(df.head(5))
