from prefect import flow


@flow
def my_flow() -> str:
    return "Hello, world!"

if __name__ == "__main__":
    print(my_flow())
