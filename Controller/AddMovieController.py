import csv

def add_movie_data(oscar, film, year, award, nomination):
    with open(oscar, mode='r', newline='', encoding='utf-8') as file:
        reader = list(csv.reader(file))
    
    header = reader[0]
    data = reader[1:]
    newFilmList = []
    isNewFilmInserted = False

    for row in data:
        # Kiểm tra xem phim đã tồn tại trong danh sách chưa
        if not isNewFilmInserted:
            newFilmList.append([0, film, year, award, nomination])
            isNewFilmInserted = True
        newFilmList.append(row)

    if not isNewFilmInserted:
        newFilmList.append([0, film, year, award, nomination])

    # Đặt lại index cho danh sách phim (bắt đầu từ 1)
    for idx, row in enumerate(newFilmList, start=1):
        row[0] = idx

    with open(oscar, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)  
        writer.writerows(newFilmList)