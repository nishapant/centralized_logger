import matplotlib.pyplot as plt
import math 
import numpy as np

# node_data = {'node1': [('1643245594.243115', '1643245594.3434398', 5), ('1643245594.343115', '1643245594.4434398', 10), ('1643245594.343115', '1643245594.3434398', 12), ('1643245594.343115', '1643245597.3434398', 12), ('1643245594.343115', '1643245597.3434398', 14), ('1643245594.337386', '1643245596.3475351', 3)]}
node_data = {'node1': [('1643604087.482788', '1643604087.483105', 208), ('1643604087.481408', '1643604089.483314', 1424), ('1643604089.643024', '1643604089.6433768', 712), ('1643604098.1992571', '1643604098.199811', 720), ('1643604101.832591', '1643604101.833057', 712), ('1643604112.6736808', '1643604112.674219', 720), ('1643604126.712826', '1643604126.713248', 712), ('1643604135.076555', '1643604135.076983', 712), ('1643604139.573515', '1643604139.5737169', 208), ('1643604139.570459', '1643604141.577307', 712), ('1643604149.781124', '1643604149.781599', 712), ('1643604152.284283', '1643604152.284491', 712), ('1643604159.84304', '1643604159.843355', 704), ('1643604161.903984', '1643604161.904263', 712), ('1643604174.8184772', '1643604174.818926', 720), ('1643604181.177727', '1643604181.178226', 712), ('1643604182.2709298', '1643604182.271224', 720), ('1643604189.3517618', '1643604189.352203', 720), ('1643604189.442858', '1643604189.443171', 712), ('1643604202.560359', '1643604202.560738', 712), ('1643604208.584957', '1643604208.585261', 712), ('1643604217.751296', '1643604217.751725', 712), ('1643604227.984179', '1643604227.984567', 712), ('1643604231.9596832', '1643604231.959934', 720), ('1643604238.331414', '1643604238.3318222', 712)], 'node2': [('1643604151.172676', '1643604151.172885', 208), ('1643604151.16476', '1643604153.176936', 704), ('1643604170.2008379', '1643604170.201074', 720), ('1643604177.3376472', '1643604177.338093', 720), ('1643604183.894124', '1643604183.8945549', 712), ('1643604191.537696', '1643604191.538097', 712), ('1643604198.180799', '1643604198.1812449', 712), ('1643604201.764257', '1643604201.7646878', 712), ('1643604206.319344', '1643604206.319635', 712), ('1643604224.713762', '1643604224.714196', 712), ('1643604227.295352', '1643604227.295809', 712), ('1643604230.334033', '1643604230.3345091', 712), ('1643604237.8163068', '1643604237.816482', 720), ('1643604248.186833', '1643604248.1873112', 712)]}

# buckets = {rounded_timestamp(round down): [len1, len2...]}
bandwidth_buckets = {} 
timedelay_buckets = {}

for node in node_data.keys():
    for data_point in node_data[node]:
        start_time, end_time, hash_len = data_point
        t_end = int(math.floor(float(end_time)))
        
        # Bandwidth
        len_int = int(hash_len)

        if t_end in bandwidth_buckets.keys():
            bandwidth_buckets[t_end].append(len_int)
        else:
            bandwidth_buckets[t_end] = [len_int]

        # Timedelay
        timedelay = float(end_time) - float(start_time)
        if t_end in timedelay_buckets.keys():
            timedelay_buckets[t_end].append(timedelay)
        else:
            timedelay_buckets[t_end] = [timedelay]


# Time Delay
timedelay_xvals = []
maxs = []
mins = []
percentile_90th = []
medians = []

print(timedelay_buckets)
for timestamp in timedelay_buckets.keys():
    delays = timedelay_buckets[timestamp]
    maxs.append(max(delays))
    mins.append(min(delays))
    percentile_90th.append(np.percentile(delays, 90))
    medians.append(np.median(delays))

    timedelay_xvals.append(timestamp)


fig = plt.figure(figsize=(12,5))
max_plt = plt.scatter(timedelay_xvals, maxs, color="teal")
min_plt = plt.scatter(timedelay_xvals, mins, color="violet")
ninety_plt = plt.scatter(timedelay_xvals, percentile_90th, color="pink")
median_plt =  plt.scatter(timedelay_xvals, medians, color="goldenrod")
plt.legend((max_plt, min_plt, ninety_plt, median_plt),
            ('Max Values', 'Min Values', 'Ninetieth Percentile Values', 'Median Values'),
            loc='upper right')
plt.xticks(np.arange(min(timedelay_xvals)-1, max(timedelay_xvals)+3, 1.0))
plt.title('Time Delay Graph')
plt.xlabel('Time (seconds)')
plt.ylabel('Time Delay (seconds)')
plt.show()


# Bandwidth plot 
bandwidth_xvals = []
bandwidth_yvals = []

for timestamp in bandwidth_buckets.keys():
    bit_length_total = sum(bandwidth_buckets[timestamp])

    bandwidth_xvals.append(timestamp)
    bandwidth_yvals.append(bit_length_total)

xtick_num = 1/len(bandwidth_xvals) * 400
fig = plt.figure(figsize=(10,5))
plt.bar(bandwidth_xvals, bandwidth_yvals, color='maroon')
plt.xticks(np.arange(min(bandwidth_xvals)-1, max(bandwidth_xvals)+1, xtick_num))
plt.title('Bandwidth Graph')
plt.xlabel('Time (seconds)')
plt.ylabel('Length of data (bits)')
plt.show()
