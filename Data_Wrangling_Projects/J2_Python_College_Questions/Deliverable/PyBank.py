f = open("budget_data.csv")
f_new = open("PyBank_Results.txt", "w")
month_count = 0
income = 0
prev_amt = 0
amt = 0
diff_count = 0
total_change = 0
greatest_inc = 0
greatest_inc_month = ""
greatest_dec = 0
greatest_dec_month = ""
for line in f:
    if month_count == 0:
        month_count += 1
        continue
    else:
        new_line = line.split(",")
        if month_count == 1:
            prev_amt = int(new_line[1])
        else:
            diff = int(new_line[1]) - prev_amt
            if diff > greatest_inc:
                greatest_inc = diff
                greatest_inc_month = new_line[0]
            elif diff < greatest_dec:
                greatest_dec = diff
                greatest_dec_month = new_line[0]
            diff_count += 1
            total_change += diff
            prev_amt = int(new_line[1])
        income += int(new_line[1])
    month_count += 1
month_count -= 1
avg_change = total_change / diff_count
f.close()
print("Financial Analysis")
f_new.write("Financial Analysis\n")
print("----------------------------")
f_new.write("----------------------------\n")
print("Total Months: ", month_count)
f_new.write("Total Months: " + str(month_count) + "\n")
print("Total: $", income)
f_new.write("Total: $" + str(income) + "\n")
print("Average Change: $", round(avg_change, 2))
f_new.write("Average Change: $" + str(round(avg_change, 2)) + "\n")
print("Greatest Increase in Profits: ", greatest_inc_month, " ($", greatest_inc, ")")
f_new.write("Greatest Increase in Profits: " + str(greatest_inc_month) + " ($" + str(greatest_inc) + ")\n")
print("Greatest Decrease in Profits: ", str(greatest_dec_month), " ($", str(greatest_dec), ")")
f_new.write("Greatest Decrease in Profits: " + str(greatest_dec_month) + " ($" + str(greatest_dec) + ")\n")


f_new.close()
