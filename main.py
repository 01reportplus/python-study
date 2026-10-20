# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    user = {
        "id":1234,
        "username":"jackie",
        "password":"admin123"
    }

    items = user.items()


    print(user.get("gender","man"))


    scores = {
        "张三": 85,
        "李四": 60,
        "王五": 95
    }

    # 筛选大于 80 分的数据
    result = {
        name: score
        for name, score in scores.items()
        if score > 80
    }

    print(result)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
