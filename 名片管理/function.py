card_list = []


def homepage():
    print("*" * 50)
    print("欢迎使用【名片管理系统】1.0")
    print(" ")
    print("1.新建名片")
    print("2.显示全部")
    print("3.查询名片")
    print(" ")
    print("0.退出系统")
    print("*" * 50)


def new_card():
    print("-" * 50)
    print("新增名片")

    name = input("请输入姓名: ")
    phone = input("请输入电话号码: ")
    qq = input("请输入QQ号码: ")
    e_mail = input("请输入电子邮件")

    card_dict = {"name": name,
                 "phone": phone,
                 "qq": qq,
                 "e_mail": e_mail}

    card_list.append(card_dict)

    print(f"添加{name}的名片成功")


def show_all():
    if len(card_list) == 0:
        print("当前没有任何名片信息，请使用新增功能添加名片。")
        return

    print("-" * 50)
    print("显示所有名片")

    for name in ["姓名", "电话", "QQ", "邮箱"]:
        print(name, end="\t\t")
    print("")
    print("=" * 50)

    for card_dict in card_list:
        print(f"{card_dict['name']}\t\t"
              f"{card_dict['phone']}\t\t"
              f"{card_dict['qq']}\t\t"
              f"{card_dict['e_mail']}")


def research_card():
    print("-" * 50)
    print("搜索名片")

    find_name = input("请输入要搜索的姓名：")

    for card_dict in card_list:
        if find_name in card_dict['name']:
            print("姓名\t\t电话\t\tQQ\t\t邮箱")
            print("=" * 50)
            print(f"{card_dict['name']}\t\t{card_dict['phone']}\t\t{card_dict['qq']}\t\t{card_dict['e_mail']}")
            deal_card(card_dict)
            break
        else:
            print(f"抱歉，没有找到{find_name}")


def deal_card(find_card):
    number = (input("请选择要执行的操作 1 修改 2 删除 0 返回上级菜单"))
    if number == "1":
        find_card['name'] = input_card_info(find_card['name'], "姓名")
        find_card['phone'] = input_card_info(find_card['phone'], "电话")
        find_card['qq'] = input_card_info(find_card['qq'], "QQ")
        find_card['e_mail'] = input_card_info(find_card['e_mail'], "邮箱")

        print("修改成功")
    elif number == "2":
        card_list.remove(find_card)
        print("删除完毕")

    else:
        pass



def input_card_info(dict_value, tip_message):
    s = input(tip_message)
    if len(s) == 0:
        return dict_value
    else:
        return s


def write_in():
    with open('database.txt', 'w') as datas:
        for line in card_list:
            datas.write(str(line) + "\n")


def write_out():
    with open('database.txt') as datas:
        for data in datas:
            card_list.append(eval(data.rstrip()))
