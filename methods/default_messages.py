#private messages
private_start = "\- Set a reminder with me by typing \-\-\> \n'/set @\<time\> \<DD/MM\> \<Task\>' \n *Example*: '/set @1300 18/05 Project Meeting' \n _If you wish to set a repeated reminder, you can add 'repeat \<duration\>' at the back such as daily/monthly/weekly/30min/2hour'_ \n\n \- View your exiting reminders by typing \-\-\> '/view'\. \n\n \- You can even remove existing reminders by typing \-\-\> '/remove'"
private_set_error = "Set a reminder with me by typing '/set @\<time\> \<DD/MM\> \<Task\>' \n *Example*: '/set @1300 18/05 Project Meeting' \n _If you wish to set a repeated reminder, you can add 'repeat \<duration\>' at the back such as daily/monthly/weekly/30min/2hour'_"
empty_reminder = "Please provide a reminder message by typing '/set @<time> <DD/MM> <Task>' \n Example:'/set @1300 18/05 Project Meeting'"
empty_date = "Please provide a reminder date by typing '/set @<time> <DD/MM> <Task>' \n Example:'/set @1300 18/05 Project Meeting'"
wrong_format_time = "Please provide a reminder time by typing '/set @<time> <DD/MM> <Task>' \n Example:'/set @1300 18/05 Project Meeting'"

#group expenses
group_set_error = "Set a reminder with me by typing '/set@SetReminderBot @\<time\> \<DD/MM\> \<Task\>' \n *Example*: '/set@SetReminderBot @1300 18/05 Project Meeting' \n _If you wish to set a repeated reminder, you can add 'repeat \<duration\>' at the back such as daily/monthly/weekly/30min/2hour'_"
group_start = "\- Set a reminder with me by typing \-\-\> \n'/set@SetReminderBot @\<time\> \<DD/MM\> \<Task\>' \n *Example*: '/set@SetReminderBot @1300 18/05 Project Meeting' \n _If you wish to set a repeated reminder, you can add 'repeat \<duration\>' at the back such as daily/monthly/weekly/30min/2hour'_ \n\n \- View your exiting reminders by typing \-\-\> '/view@SetReminderBot'\. \n\n \- You can even remove existing reminders by typing \-\-\> '/remove@SetRedminderBot'"
empty_reminder_group = "Please provide a reminder message by typing '/set@SetReminderBot @<time> <DD/MM> <Task>' \n Example:'/set@SetReminderBot @1300 18/05 Project Meeting'"
empty_date_group = "Please provide a reminder date by typing '/set@SetReminderBot @<time> <DD/MM> <Task>' \n Example:'/set@SetReminderBot @1300 18/05 Project Meeting'"
wrong_format_time_group = "Please provide a reminder time by typing '/set@SetReminderBot @<time> <DD/MM> <Task>' \n Example:'/set@SetReminderBot @1300 18/05 Project Meeting'"

#general
no_reminders = 'You have not set any reminders' 
reminders_start = 'Enter the index of the reminder you wish to remove by typing "/remove <index>" \n\n if you wish to remove all reminders, simply type "/remove all"'
invalid_time_set = 'You have entered a time or date that is in the past.'
start_msg_all = "Hello! Welcome to SetReminderBot. \n\nI am your helpful reminder bot that allows you to set a <b>ONE-LINER REMINDER</b> and will alert you about it when the set time and date arrives. \n\nI am mainly made for creating group chat reminders as most bots nowadays often require you to send parts of the details separately. This could be disruptive as the bot might take in the wrong information if another text from another group member comes in halfway through the setting process. Just simply add this bot into the group chat and type '/help' to begin and see what you can do with the bot. \n\nThis bot can also be used for personal reminders as well, by private messaging this bot directly. \n\nV1.0 \n<i>For any queries or feedback, please contact @t3dted</i>"
invalid_repeat = "<b>INVALID REPEAT.</b> \nYou can set repeats daily, weekly, monthly and time intervals such as \n '/set @1900 21/05 Project Meeting repeat 1hour' to repeat the reminder every hour "
