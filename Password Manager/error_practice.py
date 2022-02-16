#filenotfound
# try:
#     file = open("a_file.ttx")
# except FileNotFoundError:
#     file = open("a_file.txt", "w")
# else:
#     print("File found")
# finally:
#     file.close()
#     print("done")

height= float(input("Height in m"))
weight= float(input("Weight in m"))

bmi = weight/height ** 2
print(bmi)
if height > 3:
    raise ValueError("Human height should be < 3 m")
