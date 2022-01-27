import matplotlib.pyplot as plt

node_data = {'node1': [('1643245594.343115', '1643245594.3434398', 'c'), ('1643245594.337386', '1643245596.3475351', '184405163fb19027bdaea5511126da4152e67070836010275de10ab48a3ae171')]}

for node in node_data.keys():
    data = node_data[node]
    delay_xvals = []
    delay_yvals = []

    bandwidth_xvals = []
    bandwidth_yvals = []

    for start_time, end_time, hashval in data:
        time_delay = float(end_time) - float(start_time)
        message_len = len(hashval.encode('utf-8'))

        if hashval != 'c':
            delay_xvals.append(start_time)
            delay_yvals.append(time_delay)

        
        # bandwidth_xvals.append()


    # time delay
    # for x in delay_xvals:
        

    plt.plot(delay_xvals, delay_yvals, color='blue', marker='o')
    plt.title('Time Delay')
    plt.show()
