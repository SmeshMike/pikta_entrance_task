import argparse
import json

import requests

import logger as lg


def get_payment_details(ifns: int, oktmmf: int) -> dict:
    """Получает данные платёжных реквизитов по введённым коду ИФНС и муниципальному образованию с сайта ФНС РФ."""
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    r = requests.post(
        "https://service.nalog.ru/addrno-proc.json",
        headers=headers,
        data={"c": "next", "step": 1, "npKind": "fl", "ifns": ifns, "oktmmf": oktmmf},
        timeout=0.1,
    )
    print(r.status_code)
    if r.status_code == 200:
        return json.loads(r.text)["payeeDetails"]
    else:
        raise r.raise_for_status()


def get_cmd_args() -> str:
    """Парсер аргументов Кода ИФНС и Муниципального образования из командной строки."""
    parser = argparse.ArgumentParser(prog="Поисковик платёжных реквизитов")
    parser.add_argument("ifns", nargs=1, help="Код ИФНС", type=int)
    parser.add_argument("oktmmf", nargs=1, help="Муниципальное образование", type=int)
    return parser.parse_args()


if __name__ == "__main__":
    try:
        logger = lg.get_logger()
        args = get_cmd_args()
        res = get_payment_details(args.ifns, args.oktmmf)
        logger.info(res)
    except requests.exceptions.Timeout:
        logger.info("Время ожидания ответа от сервера истекло")
    except requests.exceptions.RequestException as e:
        logger.info(str(e))
