import requests
from lxml import etree
import os

def read_existing_notices(file_path):
    """读取已存在的通知内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content:
                return content.split('\n')
            return []
    except FileNotFoundError:
        return []

def write_notices(file_path, notices):
    """将通知写入文件"""
    # 确保目录存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(notices))

def get_changes_and_update(new_notices, file_path):
    """获取变化的内容并更新文件"""
    old_notices = read_existing_notices(file_path)
    
    # 如果没有旧内容，所有都是新的
    if not old_notices:
        write_notices(file_path, new_notices)
        print("文件不存在，创建新文件并写入所有内容：")
        for notice in new_notices:
            print(notice)
        return
    
    # 检查是否完全相同
    if old_notices == new_notices:
        print("无变动")
        return
    
    # 找出所有变化的内容（新增或修改的）
    changed_notices = []
    
    # 比较两个列表的对应位置
    min_len = min(len(old_notices), len(new_notices))
    
    # 检查已存在位置的内容变化
    for i in range(min_len):
        if old_notices[i] != new_notices[i]:
            changed_notices.append(new_notices[i])
    
    # 检查新增的内容
    if len(new_notices) > len(old_notices):
        for i in range(len(old_notices), len(new_notices)):
            changed_notices.append(new_notices[i])
    
    # 更新文件
    write_notices(file_path, new_notices)
    
    # 输出变化的内容
    if changed_notices:
        print("内容有更新，新增/变化的内容：")
        for notice in changed_notices:
            print(notice)

def main():
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0'
    }
    
    url_notice = "https://jw.cdu.edu.cn/"
    r_notice = requests.get(url=url_notice, headers=header)
    r_notice.encoding = r_notice.apparent_encoding
    
    html = etree.HTML(r_notice.text)
    notice_1_ = html.xpath('//div[@class="s1-r"]//li/a/h3/text()')[1].strip()
    notice_2_ = html.xpath('//div[@class="s1-r"]//li/a/h3/text()')[2].strip()
    url_1 = html.xpath('//div[@class="s1-r"]//li/a/@href')[1].strip()
    url_1_ = "https://jw.cdu.edu.cn/" + url_1
    url_2 = html.xpath('//div[@class="s1-r"]//li/a/@href')[2].strip()
    url_2_ = "https://jw.cdu.edu.cn/" + url_2
    notice_1 = notice_1_ + url_1_
    notice_2 = notice_2_ + url_2_
    # 构建新通知列表
    new_notices = [notice_1, notice_2]
    
    # 文件路径 - 使用跨平台兼容的路径
    file_path = os.path.join("send_notice", "notice.txt")
    
    # 获取变化并更新
    get_changes_and_update(new_notices, file_path)

if __name__ == "__main__":
    main()
