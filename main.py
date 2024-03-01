import pandas as pd
import os.path


def parce_file(file_name: str, delimiter: str = '7E42'):
    print('Начало обработки файла')
    # Чтение файла
    with open(file_name, 'r') as file:
        data_string = file.read()
    # Разделение на отдельные записи по разделителю
    records = [record for record in data_string.split(delimiter) if record]
    print('Файл прочитан и разделен')
    df = pd.DataFrame(records, columns=['Record'])
    # Добавление дополнительных полей
    print('Добавляю новые поля...')
    df['DAC1'] = ''
    df['DAC2'] = ''
    df['FLOW'] = ''
    df['O2'] = ''
    print('Поля добавлены')
    # Парсинг записи по 4 символа
    print('Распределяю данные по полям...')
    df['DAC1'] = df['Record'].str.slice(0, 4)
    df['DAC2'] = df['Record'].str.slice(4, 8)
    df['FLOW'] = df['Record'].str.slice(8, 12)
    df['O2'] = df['Record'].str.slice(12, 16)
    print('Распределено успешно')
    # Элементы меняются местами
    print('Данные меняются местами...')
    df['DAC1'] = df['DAC1'].apply(lambda x: f'{str(x)[-2:]}{str(x)[:-2]}')
    df['DAC2'] = df['DAC2'].apply(lambda x: f'{str(x)[-2:]}{str(x)[:-2]}')
    df['FLOW'] = df['FLOW'].apply(lambda x: f'{str(x)[-2:]}{str(x)[:-2]}')
    df['O2'] = df['O2'].apply(lambda x: f'{str(x)[-2:]}{str(x)[:-2]}')
    print('Успешно!')
    # Перевод из HEX в Int
    print('Перевод из HEX в INT...')
    df['DAC1'] = df['DAC1'].apply(lambda x: int(x, 16))
    df['DAC2'] = df['DAC2'].apply(lambda x: int(x, 16))
    df['FLOW'] = df['FLOW'].apply(lambda x: int(x, 16))
    df['O2'] = df['O2'].apply(lambda x: int(x, 16))
    print('Перевод прошел успешно!')
    # Преобразование полей FLOW и O2
    df['FLOW'] = df['FLOW'].apply(lambda x: x / 10)
    df['O2'] = df['O2'].apply(lambda x: x / 10)
    # Сохранение в csv
    print('Время сохранять файл...')
    new_file_name = 'result_file.csv'
    # if os.path.isfile(new_file_name):
    #     os.remove(new_file_name)
    df.to_csv(new_file_name, sep=';', encoding='utf-8')
    print('Файл сохранен')
    return new_file_name


if __name__ == '__main__':
    file_name = input('Введите название файла: ')
    parce_file(file_name)
