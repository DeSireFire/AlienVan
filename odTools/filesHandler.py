'''
onedrive 文件操作
'''
import onedrivesdk


# 列出项目的子项
def navigate(client, item_id = "root"):
    items = client.item(id=item_id).children.get()
    # items = client.item(id=item_id).children.request(top=3).get()
    return items._prop_list


# 查看文件的缩略图（需要PIL）
# def view_thumbnail(client, item_id):
#     from PIL import Image
#     if len(client.item(id=item_id).thumbnails.get()) == 0:
#         print("File does not have any thumbnails!\n")
#     else:
#         action = int(input("Size? 1:Small 2:Medium 3:Large... "))
#         try:
#             os.remove("./tmp_thumb.jpg")
#         except:
#             pass
#         if action == 1:
#             client.item(id=item_id).thumbnails[0].small.download("./tmp_thumb.jpg")
#         elif action == 2:
#             client.item(id=item_id).thumbnails[0].medium.download("./tmp_thumb.jpg")
#         elif action == 3:
#             client.item(id=item_id).thumbnails[0].large.download("./tmp_thumb.jpg")
#         image = Image.open("./tmp_thumb.jpg")
#         image.show()


# 复制
def paste(client, item_id, copy_item_ids):
    ref = onedrivesdk.ItemReference()
    ref.id = item_id
    for id in copy_item_ids:
        client.item(id=id).copy(parent_reference=ref).post()


# 获取分享链接
def get_sharing_link(client, item_id):
    action = int(input("Type? 1:View 2:Edit... "))
    permission = client.item(id=item_id).create_link("view" if action == 1 else "edit").post()
    return "\n{}\n".format(permission.link.web_url)


# 创建目录
def creat_folder(client, item_id, folderName):
    '''
    创建目录
    :param item_id: 字符串，新创建目录项所在的目录
    :param folderName: 字符串，新建目录名
    :return:
    '''
    f = onedrivesdk.Folder()
    i = onedrivesdk.Item()
    i.name = folderName   # 新建的文件夹名
    i.folder = f
    return client.item(drive='me', id=item_id).children.add(i)


# 重命名
def rename(client, item_id, NewItemName):
    renamed_item = onedrivesdk.Item()
    renamed_item.name = NewItemName
    renamed_item.id = item_id

    return client.item(drive='me', id=renamed_item.id).update(renamed_item)


# 删除
def delete(client, item_id):
    '''
    删除文件
    :param client:
    :param item_id:
    :return:
    '''
    confirm = input("Confirm delete? Y/N: ")
    if confirm == "Y":
        client.item(id=item_id).delete()