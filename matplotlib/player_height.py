import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from statistics import geometric_mean
import csv


def csv_open():
    # output_dict = collections.defaultdict(list)
    output_dict = {}
    output_list = []

    with open('player_height.csv', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            output_dict.setdefault(row[4], []).append(int(row[3]))
            output_list.append(int(row[3]))

    return output_dict, output_list


def scatter_prepper(color_dict):
    # Loop that adds a scatterplot for each team to ax
    player_id = 0
    for x in team_dict:
        player_range = range(player_id, len(team_dict[x]) + player_id)
        player_id += len(team_dict[x])

        ax.scatter(player_range, team_dict[x], c=color_dict[x], label=x)

    team_handles = ax.get_legend_handles_labels()[0]
    return team_handles


def st_dev(inp_iter, fdegrees=0):
    var_sum = 0
    avg = sum(inp_iter) / len(inp_iter)

    for item in inp_iter:
        var_sum += (item - avg)**2


    some = var_sum / (len(inp_iter) - fdegrees)
    st_dev = some ** 0.5
    return st_dev


def ari_mean(inp_iter):
    return sum(inp_iter) / len(inp_iter)


# Dictionary specifying team colors
color_dict = {
    'Inter': '#a29161', 'Juventus': '#000000', 'Napoli': '#12a0d7',
    'Milan': '#fb090b', 'Atalanta': '#1e71b8', 'Lazio': '#87d8f7',
    'Roma': '#8e1f2f'
}

plt.style.use('ggplot')
team_dict, height_list = csv_open()

# Using the variable ax for a single axes
fig, ax = plt.subplots(figsize=(10, 7))

team_handles = scatter_prepper(color_dict)


# Calculating and plotting arithmetic mean
arithmetic_mean = ari_mean(height_list)
amean = [arithmetic_mean for i in height_list]
amean_plot = ax.plot(range(len(amean)), amean, color='#e0233f')
amean_artist = mlines.Line2D([], [], color='#e0233f', label='Arithmetic mean')


# Calculating and plotting geometric mean
geometric_mean = geometric_mean(height_list)
gmean = [geometric_mean for i in height_list]
gmean_plot = ax.plot(range(len(gmean)), gmean, color='#2480c4', linestyle='dashed')
gmean_artist = mlines.Line2D([], [], color='#2480c4', linestyle='dashed', label='Geometric mean')


# Specifying legends
legend1 = plt.legend(handles=team_handles, loc=4)
legend2 = plt.legend(handles=[amean_artist, gmean_artist], loc=3)
ax.add_artist(legend1)
# ax.add_artist(legend2)


plt.title('Height in serie A')
plt.ylabel('Height (cm)')
plt.tight_layout()
ax.axes.get_xaxis().set_visible(False)

plt.show()