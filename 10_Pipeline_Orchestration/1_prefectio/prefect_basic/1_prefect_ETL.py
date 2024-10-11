from prefect import task, flow,Flow


@task
def extract(path):
    with open(path, "r") as file:
        text = file.readline().strip()
    data=  text.split(",")
    return data

def multi_tran(num):
    return num*num

@task
def transform(data):
    tran_data = [multi_tran(  int(i))+1 for i in data]
    return tran_data

@task
def load_text(data,path):
    import csv
    with open(path, "w") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(data)

@flow()
def main():
    data = extract(path="test.txt")
    tran_data = transform(data=data)
    load_text(tran_data,path="tran_data.csv")


main()