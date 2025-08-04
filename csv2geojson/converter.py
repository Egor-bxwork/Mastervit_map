import pandas as pd
import json

def safe_str(value):
    """
    Преобразует значение в строку, заменяя NaN на пустую строку.
    """
    if pd.isna(value):
        return ""
    return str(value)

def safe_float(value):
    """
    Преобразует значение в число, заменяя NaN на 0.0.
    """
    if pd.isna(value):
        return 0.0
    return float(value)

def safe_bool(value):
    """
    Преобразует значение в логический тип, учитывая NaN.
    """
    if pd.isna(value):
        return False
    if isinstance(value, bool):
        return value
    # Если строка вроде "True" или "False"
    return str(value).strip().lower() in ['true', '1', 'да', 'yes']

def convert_csv_to_geojson(csv_file, output_file):
    df = pd.read_csv(csv_file)

    features = []
    for idx, row in df.iterrows():
        # Проверяем наличие координат
        if pd.isna(row.get("Долгота")) or pd.isna(row.get("Широта")):
            continue  # Пропускаем строки без координат

        try:
            longitude = float(row["Долгота"])
            latitude = float(row["Широта"])
        except (ValueError, TypeError):
            continue  # Пропускаем если координаты невалидные

        feature = {
            "type": "Feature",
            "properties": {
                "id": safe_str(row.get("id", idx + 1)),
                "name": safe_str(row.get("name", f"Точка {idx + 1}")),
                "Номер": safe_str(row.get("Номер")),
                "Сумма": safe_float(row.get("Сумма")),
                "Стоимость Материала": safe_float(row.get("Стоимость Материала")),
                "Стоимость Услуги": safe_float(row.get("Стоимость Услуги")),
                "Дата Установки": safe_str(row.get("Дата Установки")),
                "Проблемный": safe_bool(row.get("Проблемный")),
                "Адрес Доставки": safe_str(row.get("Адрес Доставки")),
                "Номер Подразделения": safe_str(row.get("Номер Подразделения")),
                "Вид Забора": safe_str(row.get("Вид Забора"))
            },
            "geometry": {
                "type": "Point",
                "coordinates": [longitude, latitude]
            }
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    print(f"✅ GeoJSON успешно создан: {output_file}")

# Запуск
if __name__ == "__main__":
    convert_csv_to_geojson(
        csv_file='Заказы_пример1 2 - Заказы_пример1 2.csv',
        output_file='geojson_0.1.geojson'
    )
