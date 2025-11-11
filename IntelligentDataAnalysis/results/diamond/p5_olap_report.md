# Звіт з Практичної роботи №5: Побудова OLAP-куба

**Дата:** 2025-11-11 18:20

**Мета:** Одержання навичок у створенні простих багатомірних OLAP кубів з використанням Python та `pandas`.

## 1. Побудований OLAP-куб (фрагмент)

Побудовано куб з 5 вимірами (`year`, `quarter`, `month`, `expert_name`, `origin_name`) та 3 мірами (`Average_Price`, `Total_Sold_Count`, `Avg_Days_On_Market`).

```
                                            Average_Price  Total_Sold_Count  Avg_Days_On_Market
year quarter month expert_name origin_name                                                     
2023 1       1     Expert_1    Natural             5064.0                 7                75.0
                   Expert_2    Natural            16201.0                 0              1081.0
                               Simulant           11256.0                 1                18.0
                               Synthetic           6413.0                 1                83.0
                   Expert_3    Natural             4046.0                 5                71.0
                               Synthetic           1887.0                 0              1085.0
                   Expert_4    Natural             4302.0                 2               392.0
                               Synthetic          10385.0                 1                30.0
                   Expert_5    Natural             3789.0                 2                81.0
                               Synthetic           5779.0                 3                64.0
```

Повний куб збережено у файл: `p5_olap_cube.csv`

## 2. Демонстрація OLAP-операцій

### 2.1. Зріз (Slice)

**Запит:** *'Показати дані тільки за 2024 рік, по Expert_1'* 

```
                                            Average_Price  Total_Sold_Count  Avg_Days_On_Market
year quarter month expert_name origin_name                                                     
2024 1       1     Expert_1    Natural             6213.0                 0               719.0
                               Simulant            1374.0                 1                50.0
             2     Expert_1    Natural             4878.0                 1               101.0
                               Synthetic           4156.0                 2                62.0
                               Treated             3456.0                 1                77.0
             3     Expert_1    Natural             5985.0                 1               457.0
                               Synthetic           3400.0                 1                74.0
     2       4     Expert_1    Natural            12675.0                 1               339.0
             5     Expert_1    Natural             5424.0                 8               211.0
                               Synthetic          22406.0                 1                58.0
             6     Expert_1    Natural             3743.0                 2               317.0
                               Simulant             964.0                 0               549.0
                               Synthetic           4871.0                 1               336.0
                               Treated            11170.0                 1                80.0
     3       7     Expert_1    Natural             3224.0                 3               184.0
                               Synthetic           2376.0                 1               116.0
                               Treated             3760.0                 1                72.0
             8     Expert_1    Natural             6127.0                 3               317.0
                               Synthetic           5024.0                 1                73.0
             9     Expert_1    Natural             4622.0                 1               240.0
                               Simulant            3531.0                 0               483.0
                               Synthetic          16661.0                 1                65.0
     4       10    Expert_1    Natural             3094.0                 5                63.0
                               Simulant            1647.0                 1                59.0
                               Synthetic           3408.0                 1                64.0
             11    Expert_1    Natural             3146.0                 3               185.0
                               Synthetic           3106.0                 1                82.0
             12    Expert_1    Natural            10693.0                 4               164.0
                               Synthetic           2998.0                 1                27.0
                               Treated              500.0                 1                58.0
```

### 2.2. Деталізація (Drill-down)

**Запит:** *'Показати дані по Q1 2023 року (з деталізацією по місяцях)'* 

```
                               Average_Price  Total_Sold_Count  Avg_Days_On_Market
month expert_name origin_name                                                     
1     Expert_1    Natural             5064.0                 7                75.0
      Expert_2    Natural            16201.0                 0              1081.0
                  Simulant           11256.0                 1                18.0
                  Synthetic           6413.0                 1                83.0
      Expert_3    Natural             4046.0                 5                71.0
                  Synthetic           1887.0                 0              1085.0
      Expert_4    Natural             4302.0                 2               392.0
                  Synthetic          10385.0                 1                30.0
      Expert_5    Natural             3789.0                 2                81.0
                  Synthetic           5779.0                 3                64.0
2     Expert_1    Natural            12720.0                 1                17.0
                  Synthetic           4528.0                 1               546.0
      Expert_2    Natural             8691.0                 5               358.0
                  Simulant            2942.0                 1                43.0
                  Treated             3252.0                 1               116.0
      Expert_3    Natural             3968.0                 5               221.0
                  Synthetic            987.0                 1               162.0
      Expert_4    Natural             6191.0                 2                70.0
                  Synthetic           8590.0                 3                78.0
      Expert_5    Natural             3934.0                 3               318.0
                  Simulant            2428.0                 1               138.0
                  Synthetic           6427.0                 1                70.0
3     Expert_1    Natural             8530.0                 5               235.0
                  Synthetic           9832.0                 1                40.0
      Expert_2    Natural             8709.0                 3               533.0
                  Simulant            3784.0                 0              1014.0
                  Synthetic           6412.0                 0              1009.0
      Expert_3    Natural             7951.0                 2               556.0
                  Simulant            2624.0                 1               538.0
                  Synthetic           5074.0                 1                15.0
      Expert_4    Natural             4274.0                 2               520.0
                  Synthetic           3927.0                 1                72.0
      Expert_5    Natural            13375.0                 3               279.0
                  Synthetic           1197.0                 0              1028.0
```

### 2.3. Консолідація (Roll-up)

**Запит:** *'Показати загальні показники по роках (агрегація з місяців/кварталів)'* 

```
      Average_Price  Total_Sold_Count
year                                 
2023         6844.0               244
2024         6561.0               225
2025         6534.0               246
```

### 2.4. Обертання (Rotate / Pivot)

**Запит:** *'Показати середню ціну за 2025 рік, де рядки - Квартал/Місяць/Експерт, а стовпці - Походження каменя'* 

```
origin_name                Natural  Simulant  Synthetic  Treated
quarter month expert_name                                       
1       1     Expert_1     11716.0         -    23278.0        -
              Expert_2      3610.0         -          -   6937.0
              Expert_3      7817.0    3597.0     3968.0  14742.0
              Expert_4      4889.0    4848.0          -        -
              Expert_5      8588.0         -     8400.0   6333.0
        2     Expert_1      7812.0         -     1889.0        -
              Expert_2      8231.0    3784.0    16143.0   8901.0
              Expert_3      2392.0         -    23193.0        -
              Expert_4      1415.0         -          -   4150.0
              Expert_5      5924.0   15016.0     3826.0        -
```

## 3. Висновок

Використання `pandas.groupby()` з багаторівневим індексом дозволяє ефективно симулювати архітектуру OLAP-куба. Ми успішно створили 5-вимірний куб з 3 мірами на основі нашої 'Вітрини Даних' (`diamonds_dataset.csv`).

Було продемонстровано всі ключові OLAP-операції (Slice, Drill-down, Roll-up, Rotate), що підтверджує гнучкість `pandas` як інструменту для багатовимірного аналізу, який є альтернативою спеціалізованим серверам на кшталт `icCube`.
