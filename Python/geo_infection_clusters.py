import copy
import csv
import random

from matplotlib import pyplot
from matplotlib import colors as mcolors

def spread_disease(clusters_array, n_infected, uninfected_array, infection_radius):
    while uninfected_array:
        infected_array = [[]]
        # select random initial site, remove from uninfected and put in list of round 0
        infected_array[0].append(uninfected_array.pop(random.choice(list(uninfected_array.keys()))))
        infection_round = 0
        total_infected_in_cluster = 0
        while infected_array[infection_round]:
            infection_round += 1
            infected_array.append([])
            for infected_site in infected_array[infection_round - 1]:
                for site_id in list(uninfected_array.keys()):
                    if (int(infected_site['X']) - int(uninfected_array[site_id]['X'])) ** 2 + (
                            int(infected_site['Y']) - int(uninfected_array[site_id]['Y'])) ** 2 <= infection_radius ** 2:
                        infected_array[infection_round].append(uninfected_array.pop(site_id))
                        total_infected_in_cluster += 1
        clusters_array.append(infected_array)
        n_infected.append(total_infected_in_cluster)

def plot_stuff(clusters_to_plot, infection_radius):
    # colors = list(mcolors.CSS4_COLORS.keys())
    # random.shuffle(colors)
    for cluster in clusters_to_plot:
        infected_in_cluster = {
            'x': [],
            'y': [],
            'label': [],
        }
        round_number = 0
        while cluster[round_number]:
            for site in cluster[round_number]:
                infected_in_cluster['x'].append(site['X'])
                infected_in_cluster['y'].append(site['Y'])
                infected_in_cluster['label'].append(site['SiteID'])
            round_number += 1
        if infected_in_cluster['x']:
            pyplot.scatter(
                infected_in_cluster['x'],
                infected_in_cluster['y'],
                # color=colors.pop()
            )

    pyplot.xlabel("X Values")
    pyplot.ylabel("Y Values")
    pyplot.title("radius: " + str(infection_radius))
    pyplot.show()

full_dataset = {}
reader = csv.DictReader(open('created_csv/data2.csv'))
for row in reader:
    if row['Site_type'] == 'rural settlement':
        full_dataset[row['SiteID']] = row
        full_dataset[row['SiteID']]['X'] = int(row['X'])
        full_dataset[row['SiteID']]['Y'] = int(row['Y'])

all_infection_radii = [x * 1000 for x in range(15,17)]
clusters_per_radius = {}
for infection_radius in all_infection_radii:
    uninfected = copy.copy(full_dataset)
    clusters = []
    total_infected = []
    spread_disease(clusters, total_infected, uninfected, infection_radius=infection_radius) # infection radius is in meters

    clusters_per_radius[infection_radius] = len(clusters)
    # report
    print("number of clusters: " + str(len(clusters)))


    # plot it all
    plot_stuff(clusters, infection_radius)

pyplot.plot(list(clusters_per_radius.keys()), list(clusters_per_radius.values()), marker='o')
# pyplot.xlabel('infection radius (km)')
# pyplot.ylabel('number of clusters')
pyplot.show()
