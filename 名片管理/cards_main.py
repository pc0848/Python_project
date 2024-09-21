import function


function.write_out()

while True:
    function.homepage()
    str_1 = input("请选择操作功能")
    print(f"你选择的操作是{str_1}")

    if str_1 == "1":
        function.new_card()
    elif str_1 == "2":
        function.show_all()
    elif str_1 == "3":
        function.research_card()
    elif str_1 == "0":
        print("欢迎再次使用【名片管理系统】")
        break
    else:
        print("您输入的不正确，请再输入一遍")

function.write_in()





