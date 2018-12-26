'''
onedrive 文件操作
'''



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


# 上传
# returned_item_up = client.item(drive='me', id='root').children['README.md'].upload('/home/rq/workspace/python/AlienVan/README.md')
# returned_item_up = client.item(drive='me', id='root')
# returned_item_up_ch = returned_item_up.children['README.md']
# returned_item_up_ch_up = returned_item_up_ch.upload('/home/rq/workspace/python/AlienVan/README.md')


# 创建目录
# f = onedrivesdk.Folder()
# i = onedrivesdk.Item()
# i.name = '测试文件夹'   # 新建的文件夹名
# i.folder = f
# returned_item_path = client.item(drive='me', id='root').children.add(i)


# 重命名
# renamed_item = onedrivesdk.Item()
# renamed_item.name = 'NewItemName'
# renamed_item.id = 'root'
#
# new_item = client.item(drive='me', id=renamed_item.id).update(renamed_item)


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