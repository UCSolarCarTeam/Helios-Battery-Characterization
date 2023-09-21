import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta as td

# Read the data from the CSV file
df = pd.read_csv("Cycle Test.csv")

cell_lookup = '01-01-02'

def find_cell(cell_lookup, df):
    cells = df["Cell Number"]
    for index, value in cells.iloc[:].items():
        if value == cell_lookup:
            start = index + 1
            cell = value
            break
    return(start, cell)
    
def SOC(df, start):
    return df.iloc[start + 1][1]

def current_sweep(df, start):
    label = df['Date & Time']
    for index, value in label.iloc[start:].items():
        if value == 'Current Sweep':
            start = index + 1
        if value == "AC Impedance":
            end = index - 1
            break

    current = df['Current'][start:end + 1].tolist()

    clean_current = pd.to_numeric(current, errors='coerce')

    voltage = df["Voltage"][start:end + 1].tolist()

    clean_voltage = pd.to_numeric(voltage, errors='coerce')

    time_og = df["Date & Time"][start:end + 1].tolist()


    time_dif = [0]
    time1 = datetime.strptime(time_og[0], "%d-%m-%Y %H:%M:%S")

    for point in range(0,len(time_og)-1):
        time2 = datetime.strptime(time_og[point + 1], "%d-%m-%Y %H:%M:%S")
        time = time2 - time1
        time_dif.append(td.total_seconds(time))
    

    return(clean_current, clean_voltage, time_dif)

def ac_impeadance(df, start):
    label = df['Date & Time']
    for index, value in label.iloc[start:].items():
        if value == 'AC Impedance':
            start = index + 1
        if value == "End Test":
            end = index - 1
            break

    current = df['Current'][start:end + 1].tolist()

    clean_current = pd.to_numeric(current, errors='coerce')

    voltage = df["Voltage"][start:end + 1].tolist()

    clean_voltage = pd.to_numeric(voltage, errors='coerce')

    time_og = df["Date & Time"][start:end + 1].tolist()

    time_dif = [0]
    time1 = datetime.strptime(time_og[0], "%d-%m-%Y %H:%M:%S")

    for point in range(0,len(time_og)-1):
        time2 = datetime.strptime(time_og[point + 1], "%d-%m-%Y %H:%M:%S")
        time = time2 - time1
        time_dif.append(td.total_seconds(time))

    return(clean_current, clean_voltage, time_dif)


    

try:
    start, cell = find_cell(cell_lookup, df)
    print(start)

    print(cell)

    print(f'SOC {SOC(df, start)}')

    cs_current, cs_voltage, cs_time = current_sweep(df, start)

    print(f'current sweep current {len(cs_current)} \n current sweep voltage {len(cs_voltage)} \n current sweep time {len(cs_time)}')

    ai_current, ai_voltage, ai_time = ac_impeadance(df, start)

    print(f'ac impeadance current {len(ai_current)} \n ac impeadance voltage {len(ai_voltage)} \n ac impedance time {len(ai_time)}')

except UnboundLocalError:
    print('Cell Not Found')

fig, axs = plt.subplots(1, 2, figsize=(12, 6))

#
# Plot the first graph (Voltage vs. Time)
axs[0].plot(cs_time, cs_voltage, marker='o', linestyle='-', color='blue', label='Voltage')
axs[0].set_xlabel('Time')
axs[0].set_ylabel('Voltage', color='blue')
axs[0].tick_params(axis='y', labelcolor='blue')
axs[0].set_title('Current Sweep')

# Create a secondary y-axis for the first subplot (Current)
ax2 = axs[0].twinx()
ax2.plot(cs_time, cs_current, marker='s', linestyle='--', color='green', label='Current')
ax2.set_ylabel('Current', color='green')
ax2.tick_params(axis='y', labelcolor='green')

# Plot the second graph (Voltage vs. Time)
axs[1].plot(ai_time, ai_voltage, marker='o', linestyle='-', color='blue', label='Voltage')
axs[1].set_xlabel('Time')
axs[1].set_ylabel('Voltage', color='blue')
axs[1].tick_params(axis='y', labelcolor='blue')
axs[1].set_title('AC Impendance')

# Create a secondary y-axis for the second subplot (Current)
ax3 = axs[1].twinx()
ax3.plot(ai_time, ai_current, marker='s', linestyle='--', color='green', label='Current')
ax3.set_ylabel('Current', color='green')
ax3.tick_params(axis='y', labelcolor='green')

# Rotate x-axis labels for better readability (adjust the rotation angle as needed)
axs[0].tick_params(axis='x', rotation=45)
axs[1].tick_params(axis='x', rotation=45)

# Adjust the layout
plt.tight_layout()

# Show the plots
plt.show()

