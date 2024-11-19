import csv

def add_movie_data(oscar, film, year, award, nomination):
    with open(oscar, mode='r', newline='', encoding='utf-8') as file:
        reader = list(csv.reader(file))
    
    header = reader[0]
    data = reader[1:]
    newFilmList = []
    added = False

    for row in data:
        if not added:
            newFilmList.append([0, film, year, award, nomination])
            added = True
        
        newFilmList.append(row)

    for idx, row in enumerate(newFilmList, start=1):
        row[0] = str(idx)

    with open(oscar, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)  
        writer.writerows(newFilmList)
