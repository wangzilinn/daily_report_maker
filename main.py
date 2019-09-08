import tkinter as tk
import time
import datetime
from tkinter import messagebox


class Framework(tk.Tk):
    """框架结构"""
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.__place_weight()
        self.daily_report = DailyReport()
        self.protocol("WM_DELETE_WINDOW", self.__on_closing)

    def __place_weight(self):
        """放置各种weight"""
        # 开始按钮
        self.button_start_task = tk.Button(self, text="start", command=self.__command_button_start_task)
        self.button_start_task.grid(row=0, column=0)
        # 停止按钮
        self.button_stop_task = tk.Button(self, text="stop", command=self.__command_button_stop_task)
        # 默认隐藏停止按钮
        self.button_stop_task.grid_forget()
        # 任务名输入框
        self.entry_task_name_input = tk.Entry(self)
        self.entry_task_name_input.grid(row=0, column=1)
        # 输出日报按钮
        self.button_output_report = tk.Button(self, text="output", command=self.__command_button_output_report)
        self.button_output_report.grid(row=0, column=2)
        # 日报输出框
        self.text_daily_report = tk.Text(self)
        self.text_daily_report.grid_forget()
        # 根据自定义的日报计算总时间
        self.button_regenerate_daily_report = tk.Button(self, text="regenerate", command=self.__command_button_regenerate_daily_report)
        self.button_regenerate_daily_report.grid_forget()
        # 关闭日报输出框按钮
        self.button_close_daily_report_text = tk.Button(self, text="close", command=self.__command_button_close_daily_report_text)
        self.button_close_daily_report_text.grid_forget()
        # save和load按钮
        self.button_save_daily_report = tk.Button(self, text="save", command=self.__command_button_save_daily_report)
        self.button_save_daily_report.grid(row=0, column=3)
        self.button_load_daily_report = tk.Button(self, text="load", command=self.__command_button_load_daily_report)
        self.button_load_daily_report.grid(row=0, column=4)

    def __command_button_start_task(self):
        if DailyReport.task_status == "running":
            self.__command_button_stop_task()
            return
        task_name = self.entry_task_name_input.get()
        self.entry_task_name_input.delete(0, tk.END)  # 清空当前任务名,以便输入新的任务
        if task_name == "":
            print("任务名为空")
            return
        # 如果任务名有效, 则开始进行一个新任务:
        # 隐藏开始按钮,显示停止按钮
        self.entry_task_name_input.grid_forget()
        self.button_stop_task.grid(row=0, column=1)
        self.daily_report.add_new_task(task_name)

    def __command_button_stop_task(self):
        self.button_stop_task.grid_forget()
        self.entry_task_name_input.grid(row=0, column=1)
        self.daily_report.stop_current_task()

    def __command_button_output_report(self):
        if DailyReport.task_status == "running":
            self.__command_button_stop_task()
        self.text_daily_report.delete("0.0", "end")
        daily_report_text = self.daily_report.get_daily_report()
        self.text_daily_report.grid(row=1, column=0, columnspan=3)
        self.text_daily_report.insert("0.0", daily_report_text)
        self.button_regenerate_daily_report.grid(row=2, column=0)
        self.button_close_daily_report_text.grid(row=2, column=1)

    def __command_button_regenerate_daily_report(self):
        original_text = self.text_daily_report.get("0.0", "end")
        self.text_daily_report.delete("0.0", "end")
        output_text = self.daily_report.regenerate_daily_report(original_text)
        self.text_daily_report.insert("0.0", output_text)

    def __command_button_close_daily_report_text(self):
        self.text_daily_report.grid_forget()
        self.button_regenerate_daily_report.grid_forget()
        self.button_close_daily_report_text.grid_forget()

    def __command_button_save_daily_report(self):
        if DailyReport.task_status == "running":
            self.__command_button_stop_task()
        file = open("data.txt", "w")
        file.write(DailyReport.task_details_string)
        file.close()

    def __command_button_load_daily_report(self):
        file = open("data.txt", "r")
        DailyReport.task_details_string = file.read()
        file.close()

    def __on_closing(self):
        """关闭确认"""
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()


class DailyReport:

    output_string = ""
    task_details_string = ""
    total_time = 0
    previous_task_start_times_string = ""  # 上一个任务开始的时间的字符串形式
    task_status = "stop"
    current_task_name = ""

    def __init__(self):
        current_date = time.strftime("%m/%d", time.localtime())
        name = "王子林"
        DailyReport.output_string = current_date + " " + name + " 本日进展"

    @staticmethod
    def add_new_task(task_name):
        DailyReport.current_task_name = task_name
        DailyReport.task_status = "running"
        DailyReport.previous_task_start_times_string = time.strftime("%H:%M", time.localtime())

    @staticmethod
    def stop_current_task():
        DailyReport.task_status = "stop"
        #DailyReport.total_time += current_time_stamp - DailyReport.previous_task_start_timestamp
        # 在日报中添加一行任务
        current_time_string = time.strftime("%H:%M", time.localtime())
        DailyReport.task_details_string += DailyReport.previous_task_start_times_string \
                                        + "~" + current_time_string \
                                        + " " + DailyReport.current_task_name \
                                        + "\n"

    @staticmethod
    def get_total_time(task_details_string):
        """之所以分析整段日报来算时间,是想要可以自定义日报"""
        total_time = 0

        def get_time_difference(start_time, end_time):
            start_time = time.strptime(start_time, "%H:%M")
            end_time = time.strptime(end_time, "%H:%M")
            start_datetime = datetime.datetime(1996, 11, 12, start_time[3], start_time[4], 0)
            end_datetime = datetime.datetime(1996, 11, 12, end_time[3], end_time[4], 0)
            return (end_datetime - start_datetime).total_seconds()

        # task_details_string = "16:47~17:47 学习python\n17:48~18:49 1234\n"
        # 去除末尾\n
        daily_report_string = task_details_string[:-1]
        task_string_array = daily_report_string.split("\n")
        for single_task_string in task_string_array:
            single_time_string = single_task_string.split(" ", 1)
            single_time_string_array = single_time_string[0].split("~")
            # print(single_time_string_array)
            total_time += get_time_difference(single_time_string_array[0], single_time_string_array[1])
            # print(single_time_string_array)

        m, s = divmod(total_time, 60)
        h, m = divmod(m, 60)

        return "%02d小时%02d分" % (h, m)

    @staticmethod
    def get_daily_report():
        total_time_string = "总时间:" + DailyReport.get_total_time(DailyReport.task_details_string)
        return DailyReport.output_string \
                + "\n" \
                + DailyReport.task_details_string \
                + total_time_string \
                + "\n" \
                + "感想:"

    @staticmethod
    def regenerate_daily_report(original_daily_report):
        original_daily_report_array = original_daily_report.split("\n")
        task_details_array = original_daily_report_array[1:-3]
        task_detail_string = ""
        for task_detail in task_details_array:
            task_detail_string += task_detail + "\n"
        print(task_detail_string)
        total_time_string = "总时间:" + DailyReport.get_total_time(task_detail_string)
        original_daily_report_array[len(original_daily_report_array) - 3] = total_time_string
        output_daily_report = ""
        for item in original_daily_report_array:
            output_daily_report += item + "\n"
        return output_daily_report[:-2]


window = Framework()
window.title("daily report")
window.mainloop()