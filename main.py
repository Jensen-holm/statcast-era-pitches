from statcast.update import update_statcast
import datetime


def yesterday() -> datetime.date:
    return datetime.datetime.now().date() - datetime.timedelta(days=1)


def main() -> None:
    updated_df = update_statcast(date=yesterday())
    print(updated_df.describe())


if __name__ == "__main__":
    _ = main()
