f = open("election_data.csv")
f_new = open("PyPoll_Results.txt", "w")
candidate = dict()
total_votes = 0
for line in f:
    if total_votes == 0:
        total_votes += 1
        continue
    else:
        new_line = line.split(",")
        if new_line[2] not in candidate:
            candidate[new_line[2]] = 1
        else:
            candidate[new_line[2]] += 1
    total_votes += 1
f.close()
total_votes -= 1
print("Election Results")
f_new.write("Election Results\n")
print("----------------------------")
f_new.write("----------------------------\n")
print("Total Votes: ", total_votes)
f_new.write("Total Votes: " + str(total_votes) + "\n")
print("----------------------------")
f_new.write("----------------------------\n")
max_votes = 0
winner = ""
for k, v in candidate.items():
    print(k.strip("\n"), ": ", round(v / total_votes * 100, 3), "% (", v, ")")
    f_new.write(k.strip("\n") + ": " + str(round(v / total_votes * 100, 3)) + "% (" + str(v) + ")\n")
    if v > max_votes:
        max_votes = v
        winner = k
print("----------------------------")
f_new.write("----------------------------\n")
print("Winner: ", winner.strip("\n"))
f_new.write("Winner: " + winner)
print("----------------------------")
f_new.write("----------------------------\n")
f_new.close()
