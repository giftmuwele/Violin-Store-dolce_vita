score = int(input("Enter the score you got in ICT : "))

if score >= 90:
  grade = "A"
elif score >= 80:
  grade = "B"
elif score >= 70:
  grade = "C"
elif score >= 60:
  grade = "D"
else:
  grade = "F"

print("You score is :", grade)