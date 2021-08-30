from matplotlib import pyplot as plt
import csv


def arithmetic_mean(iterable):
    return sum(iterable) / len(iterable)


def csv_loader():
    # Loading name and height from Roma players into list of nested tuples
    with open('roma_height.csv', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        input_list = []  # Initiating list
        for row in csv_reader:  # Looping over every row in csv
            input_list.append((row[0], int(row[3])))  # Add tuple
    return input_list


def data_prepper(iterable):
    # Sorting tuples in player list on height
    iterable = sorted(player_list, key=lambda x: x[1])

    # Using list comprehension to create a list of only player heights
    height_list = [i[1] for i in iterable]

    # Using list comprehension to create a list of only player names
    name_list = [i[0] for i in iterable]

    # Creating a list to be used as x values
    player_index = list(range(1, len(height_list)+1))
    return height_list, name_list, player_index


# Loading data as list of nested tuples [(name1, height1), (name2, height2),]
player_list = csv_loader()

# Sorting player_list and returning non-nested lists
heights, names, index = data_prepper(player_list)

# Getting arithmetic mean from function
ari_mean = arithmetic_mean(heights)

# Setting chart style to predefined style "ggplot"
plt.style.use('ggplot')

# Creating a subplot
fig, ax = plt.subplots()

# Specifying bar chart and horizontal line
ax.bar(index, heights, label='Player height', color='#8e1f2f')
ax.hlines(ari_mean, 0, index[-1] + 1, label='Arithmetic mean', color='#CD8232')

# Specifying that a legend should be drawn
ax.legend()

# Set-up for the names on x-axis
ax.set_xticks(index)
ax.set_xticklabels(names, rotation=90)

# Adjusting where the x and y-axis begin/end
ax.set_xlim(xmin=0, xmax=index[-1] + 1)
ax.set_ylim(ymin=165, ymax=200)

plt.title('Player height in AS Roma')
plt.tight_layout()
plt.show()
