ora = str(input("Escribe una frase o palabra: "))
or_min = ora.lower()
or_se = ""
in_or = ""
l = len(or_min)
for i in range(0, l):
    if (or_min[i] != " "):
        or_se = or_se + or_min[i]
l_ii = len(or_se)
for i in range(l_ii-1,-1,-1):
    in_or = in_or + or_se[i]

print("\n - Minusculas y sin espacios: ", or_se)
print(" - Inversa: ",in_or,"\n")

if (in_or == or_se):
    print("Tu texto es un Palindromo")
else:
    print("Tu texto no es un Palindromo")