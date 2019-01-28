import datetime
import matplotlib.pyplot as plt
import pandas as pd

def plot_data(data):
    # print(len(data))
    days = len(data) if len(data) < 7 else 7
    f, axarr = plt.subplots(days)
    p = 0
    sorted_dates = list(data.keys())
    sorted_dates.sort()
    sorted_dates = sorted_dates[-days:]
    for i in sorted_dates:
        time = data[i]['time']
        x = list(map(lambda x: datetime.datetime.combine(i,x), time))
        y = data[i]['value']
        # print(x,y)
        axarr[p].plot_date(x, y, '-', marker='.', drawstyle='steps-post')
        axarr[p].set_ylim(0, 6)
        axarr[p].grid(True)
        s_hr = data[i]['total']['s'].seconds//3600
        s_min = (data[i]['total']['s'].seconds//60)%60
        a_hr = data[i]['total']['a'].seconds//3600
        a_min = (data[i]['total']['a'].seconds//60)%60
        f_hr = data[i]['total']['f'].seconds//3600
        f_min = (data[i]['total']['f'].seconds//60)%60
        axarr[p].set_title(str(i.date()) + ' = sleep-{}:{};awake-{}:{};feed-{}:{}'.format(s_hr,s_min,a_hr,a_min,f_hr,f_min), fontsize=10)
        p = p + 1
    plt.setp(axarr, yticks=[2, 3, 4], yticklabels=['sleep', 'awake', 'feed'])
    plt.gcf().autofmt_xdate()
    plt.subplots_adjust(hspace=.3, bottom = 0.1, top=.95)
    plt.show()

def get_data():
    df = pd.read_excel('sleep_cycle.xlsx')

    dates = list(df.keys())
    data = {}
    # print(dates)
    for i in range(0,len(dates),2):
        # print(dates[i], " - ##############")
        data[dates[i]] = {'event':None , 'value':[], 'time':None, 'total':{'s':datetime.timedelta(0,0), 'f':datetime.timedelta(0,0), 'a':datetime.timedelta(0,0)}}
        data[dates[i]]['time'] = [x for x in list(df.get(dates[i])) if str(x) != 'nan']
        data[dates[i]]['event'] = [x for x in list(df.get(dates[i+1])) if str(x) != 'nan']

        pm = False
        midnight = True
        prev_hour = 0
        for j in range(0,len(data[dates[i]]['time'])):
            # print(data[dates[i]]['time'][j].hour, pm)
            if midnight:
                if data[dates[i]]['time'][j].hour == 12:
                    data[dates[i]]['time'][j]=data[dates[i]]['time'][j].replace(hour=0)
                else:
                    midnight = False
            if prev_hour > data[dates[i]]['time'][j].hour:
                pm = True
            if pm:
                hr = data[dates[i]]['time'][j].hour
                # print(hr)
                data[dates[i]]['time'][j] = data[dates[i]]['time'][j].replace(hour=hr+12)
            prev_hour = data[dates[i]]['time'][j].hour

        if data[dates[i]]['time'][0] != datetime.time(0,0):
            data[dates[i]]['time'] = [datetime.time(0,0)] + data[dates[i]]['time']
            data[dates[i]]['event'] = [data[dates[i]]['event'][0]] + data[dates[i]]['event']
        if data[dates[i]]['time'][-1] != datetime.time(23,59):
            data[dates[i]]['time'] = data[dates[i]]['time'] + [datetime.time(23,59)]
            data[dates[i]]['event'] = data[dates[i]]['event'] + [data[dates[i]]['event'][-1]]

        prev_event = None
        prev_time = None
        for j in range(0, len(data[dates[i]]['event'])):
            if data[dates[i]]['event'][j] == 's':
                data[dates[i]]['value'].append(2)
            elif data[dates[i]]['event'][j] == 'a':
                data[dates[i]]['value'].append(3)
            elif data[dates[i]]['event'][j] == 'f':
                data[dates[i]]['value'].append(4)

            if prev_event:
                curr_date_time = datetime.datetime.combine(datetime.datetime.now(), data[dates[i]]['time'][j])
                prev_date_time = datetime.datetime.combine(datetime.datetime.now(), prev_time)
                data[dates[i]]['total'][prev_event] += curr_date_time - prev_date_time

            prev_event = data[dates[i]]['event'][j]
            prev_time = data[dates[i]]['time'][j]

    return data

if __name__ == '__main__':
    data = get_data()
    # print(data)
    plot_data(data)
