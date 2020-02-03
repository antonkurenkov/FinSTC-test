# -*- coding: utf-8 -*-
import os
import xmlschema
import lxml.etree as ET
import datetime


"""
Задание: Сделать скрипт на Python, в котором можно бы было задавать следующие входные данные:
- путь к xml файлу;
- путь к xsd файлу (по этой схеме должен быть сформирован xml файл);
- путь к xslt файлу и имя результирующего файла (тоже xml).
Скрипт должен взять xml файл по пути, провалидировать его по xsd схеме, затем произвести xslt трансформацию по xslt, 
затем результат провалидировать по xsd схеме (результирующий хмл также должен соответствовать некоему классу xsd схемы) и сохранить результирующий xml в файл.
Нужно предусмотреть обработку эксепшенов и ведение лога по каждой операции (валидация входящего xml, xslt трансформация, валидация результата).

"""

"""
Поскольку в условии не указан конкретный формат, в котором предполагается вводить вспомогательные схемы и файлы, 
допустим, что их названия перечислены в вспомогательном текстовом файле config.txt и лежат в одной папке с исполняемым файлом

"""

def validate_xml(xml_path, schema_xsd_path, key=None):
    """

    :param xml_path: Путь к проверяемому на соответствие схеме xls файлу
    :param schema_xsd_path: Путь к схеме, в соответствии с которой будет проверен xml файл
    :param key: вспомогательный ключ для идентификации этапа валидации
    :return: None
    """
    my_schema = xmlschema.XMLSchema(schema_xsd_path)
    try:
        my_schema.validate(xml_path)
        if my_schema.is_valid(xml_path):
            log(f'OK, XML {key} {xml_path} matches {schema_xsd_path} schema!')
    except Exception as e:
        log(f'ERROR, {e.__class__.__name__} on {xml_path} with schema {schema_xsd_path}')
        print()
        print(e.__doc__)

def transform_xml(input_xml_path, xsl_path, output_xml_path):
    """

    :param input_xml_path: Путь к исходному файлу, подлежащему трансформации в соответствии с шаблоном
    :param xsl_path: Путь к шаблону, в соответствии с которым будет трансформирован исходный файл
    :param output_xml_path: Путь, по которому будет сохранен новый файл после преобразования
    :return: Возвращает True, если преобразование прошло без ошибок, в противном случае - None
    """
    try:
        dom = ET.parse(input_xml_path)
        xslt = ET.parse(xsl_path)
        transform = ET.XSLT(xslt)
        newdom = transform(dom)

        with open(output_xml_path, 'wb+') as f:
            newdom.write(f, pretty_print=True)
        log(f'OK, transform XML on {input_xml_path} with schema {xsl_path}')
        return True
    except Exception as e:
        log(f'ERROR, {e.__class__.__name__} on {input_xml_path} with schema {xsl_path}')
        print()
        print(e.__doc__)

def log(*args):
    """
    Функция получает на вход строку с результатом действия и вносит ее в файл log.txt
    """

    with open('log.txt', 'a') as loglog:
        x = datetime.datetime.now()
        for arg in args:
            loglog.write(x.strftime("%x") + ' ' + x.strftime("%X") + ' ' + arg + '\n')
            print(x.strftime("%x") + ' ' + x.strftime("%X") + ' ' + arg)


def main():
    with open('config.txt') as file:
        if file:
            config = [os.path.join(os.getcwd(), line.strip()) for line in file.readlines()]

    if len(config) == 5:
        input_xml_path = config[0]
        output_xml_path = config[1]
        schema_xsd_path_in = config[2]
        schema_xsd_path_out = config[3]
        xsl_path = config[4]

        validate_xml(input_xml_path, schema_xsd_path_in, key='input')
        if transform_xml(input_xml_path, xsl_path, output_xml_path):
            validate_xml(output_xml_path, schema_xsd_path_out, key='output')
    else:
        print('Be sure if config file contains enough valid names!')

if __name__ == '__main__':
    main()
