from matplotlib import pyplot as plt
import csv


def arithmetic_mean(iterable):
    return sum(iterable) / len(iterable)


def geometric_mean(iterable):
    total = 1
    for x in iterable:
        total *= x  # Multiply x with total and assign new value to total
    return total ** (1 / len(iterable))  # Returning n:th root of total


def csv_loader():
    # Loading name and height from Roma players into list of nested tuples
    with open('juventus_wages.csv', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        input_list = []  # Initiating list
        next(csv_reader)  # Skipping first line with the headers
        for row in csv_reader:  # Looping over every row in csv
            input_list.append((row[0], int(row[2])))  # Add tuple
    return input_list


player_list = csv_loader()
player_list = sorted(player_list, key=lambda x: x[1])
wages = [i[1] for i in player_list]
names = [i[0] for i in player_list]
index = list(range(1, len(player_list)+1))

plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=[10, 10])

amean = arithmetic_mean(wages)
gmean = geometric_mean(wages)


# Specifying bar chart and horizontal lines
ax.bar(index, wages, color='black')
ax.hlines(
    amean, 0, len(player_list)+1,
    color='#CF3A30', label='Arithmetic mean')
ax.hlines(
    gmean, 0, len(player_list)+1,
    color='#30C5CF', label='Geometric mean')


# Customizing ticks on y axis
plt.yticks(
    [200, 400, 600, 800, 1000, amean, gmean],
    ['£200K', '£400K', '£600K', '£800K', '£1000K',
     f'£{amean:.0f}K', f'£{gmean:.0f}K']
)

# Set-up for the names on x-axis
ax.set_xticks(index)
ax.set_xticklabels(names, rotation=90)

# Adjusting scale for x axis
ax.set_xlim(xmin=0, xmax=index[-1] + 1)


plt.legend()
plt.title('Juventus weekly wages')
plt.tight_layout()
plt.show()
