from prefect import flow


@flow
def my_flow():
    print("Hello Monday Data!")


"""
20: Minute (20th minute)
8: Hour (8 AM)
*: Every day of the month
*: Every month
1: Monday (where 0 is Sunday, 1 is Monday, and so on)
"""

if __name__ == "__main__":
    my_flow.serve(name="prepare_data", cron="20 8 * * 1")
