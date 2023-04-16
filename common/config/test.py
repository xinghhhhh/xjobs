from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor,Future
import common.config.global_info as global_info
import time
from datetime import datetime

# class hhh(ThreadPoolExecutor):
#     def __init__(self):
#         self._work_queue = super.__init__.__name__
#
#
#     def get(self):
#         print(len(super._work_queue))
#         return len(super._work_queue)


batch_date = global_info.global_dict['batch_date']
print(batch_date)
print("2222222222222222222222")
batch_date1 = datetime.strptime(batch_date, '%Y%m%d')
batch_date2 = datetime.strftime(batch_date1, '%Y-%m-%d')
batch_date3 = datetime.strptime(batch_date2, '%Y-%m-%d')
print(batch_date3)

exit(0)
t_pool = ThreadPoolExecutor(max_workers=2)


def gg(tt):
    print("00000")
    time.sleep(tt)


t_pool.submit(gg,3)
t_pool.submit(gg,6)

t_pool.submit(gg,8)
t_pool.submit(gg,23)
t_pool.submit(gg,9)
t_pool.submit(gg,1)
t_pool.submit(gg,8)

print(t_pool._work_queue.qsize())
print("==========================")

while True:
    print(t_pool._work_queue.qsize())
    time.sleep(3)