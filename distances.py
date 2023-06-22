# %%
# 2023-6-13 16:24:00
# 35.560468  139.547458
# 35.560656  139.546283
# 20230613_162001_AIC 2_10Hz
import math
import csv
import datetime
import os

# %%
def calculate_distance(lat1, lon1, lat2, lon2):
    # 地球の半径（単位: メートル）
    earth_radius = 6371000.0

    # 度数法からラジアンに変換
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # ヒュベニの公式を用いて距離を計算
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c

    return distance

# %%
def get_start_and_goal_time():
    # 年月日時分秒の入力
    input_date_str = input("年月日時分秒を入力してください (YYYY-MM-DD HH:MM:SS): ")

    # 入力された文字列をdatetimeオブジェクトに変換
    input_date = datetime.datetime.strptime(input_date_str, "%Y-%m-%d %H:%M:%S")

    # 入力されたdatetimeオブジェクトを表示
    print("入力された日付と時刻:", input_date)

    raw_start_time = input_date
    raw_goal_time = raw_start_time + datetime.timedelta(seconds=8)

    start_time = raw_start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    goal_time = raw_goal_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    print("Start Time:", start_time)
    print("Goal Time:", goal_time)

    return start_time, goal_time

# %%
# csvからスタートとゴールの座標を取得

def get_coordinate_from_csv(csv_file, start_time, goal_time):
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == start_time:
                start_lat = row[2]
                start_lon = row[3]
                break
        start_lat = float(start_lat)
        start_lon = float(start_lon)

    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == goal_time:
                goal_lat = row[2]
                goal_lon = row[3]
                break
        goal_lat = float(goal_lat)
        goal_lon = float(goal_lon)

    #動作確認のためのコード
    if start_lat is not None and start_lon is not None:
        print("start_lat:", start_lat)
        print("start_lon:", start_lon)
    else:
        print("指定された開始時間が見つかりませんでした。")

    if goal_lat is not None and goal_lon is not None:
        print("goal_lat:", goal_lat)
        print("goal_lon:", goal_lon)
    else:
        print("指定された開始時間が見つかりませんでした。")

    return start_lat, start_lon, goal_lat, goal_lon


# %%
def get_distances():
    csv_directory = "csv_file"  # CSVファイルが格納されているディレクトリのパス
    distances = []
    # 指定されたディレクトリ内のすべてのファイルを走査し、CSVファイルの相対パスを取得する
    csv_files = [os.path.join(csv_directory, file) for file in os.listdir(csv_directory) if file.endswith(".csv")]

    start_time, goal_time = get_start_and_goal_time()

    # 結果を個人と紐づけてdistanceに入れる必要あり
    for csv_file in csv_files:
        start_lat, start_lon, goal_lat, goal_lon = get_coordinate_from_csv(csv_file, start_time, goal_time)
        distance = calculate_distance(start_lat, start_lon, goal_lat, goal_lon)
        print("あなたの８秒間で走った距離は", distance, "メートルです。")
        distances.append(distance)

    return distances


