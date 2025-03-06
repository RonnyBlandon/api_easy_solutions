salario = 5120.0
aumento = 0.1
years = 70

result = 0.0

for num in range(0, years):
    salario = salario*(1+aumento)

print(f"Este es el salario en {years} años: {salario}")