import pandas
import re
import sys
import os


def transform(filename: str) -> list:
    messages = []
    message_regex = r"^([0-9]{1,2}/[0-9]{1,2}/[0-9]{2}, [0-9]{1,2}:[0-9]{1,2}) - ([^:]*): (.*)"
    no_message_regex = r"^[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}, [0-9]{1,2}:[0-9]{1,2} - "
    with open(filename) as fh:
        message = {}
        for line in fh:
            if matches := re.match(message_regex, line):
                message = {"datetime": matches.group(1), "user": matches.group(2), "content": matches.group(3)}
                messages.append(message)
            elif re.match(no_message_regex, line):
                continue
            else:  # multiline comments
                message["content"] = f'{message.get("content")}{line}'
    return messages


def check_args():
    if len(sys.argv) != 2:
        raise ValueError('Passe como parâmetro o caminho para o arquivo exportado do WhatsApp.')
    filename = sys.argv[1]
    if not os.path.isfile(filename):
        raise ValueError(f"Arquivo inválido: '{filename}'")


if __name__ == '__main__':
    check_args()
    data = transform(sys.argv[1])
    df = pandas.DataFrame(data)
    df['datetime'] = pandas.to_datetime(df['datetime'], format="%m/%d/%y, %H:%M")
    for year, row in df.groupby(pandas.Grouper(key='datetime', freq='Y')):
        print(year)
        print("-----------------------------------------")
        print(row["user"].value_counts())
        print(f"Total messages: {len(row)}")
        print("=========================================\n")

