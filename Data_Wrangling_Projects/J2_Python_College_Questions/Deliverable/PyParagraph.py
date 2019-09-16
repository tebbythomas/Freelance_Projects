f = open("paragraph_3.txt", "r")
string = ""
for line in f:
    #print("Each line of file")
    #print(line)
    string += line
f.close()
len_word = 0
words = string.split(" ")
for word in words:
    word = word.strip(".")
    word = word.strip(",")
    len_word += len(word)
print("Paragraph Analysis")
print("------------------")
print("Approximate Word Count: ", len(words))
sentence_count = 0
sentences = string.split(".")
for s in sentences:
    if s != "\n":
        sentence_count += 1
print("Approximate Sentence Count: ", sentence_count)
print("Average Letter Count: ", round(len_word / len(words), 1))
print("Average Sentence Length: ", round(len(words) / sentence_count, 1))
