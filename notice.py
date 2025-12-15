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
    """获取变化的内容并更新文件，返回变化的内容列表"""
    old_notices = read_existing_notices(file_path)
    
    # 如果没有旧内容，所有都是新的
    if not old_notices:
        write_notices(file_path, new_notices)
        if new_notices:
            print("首次运行，所有内容均为新增：")
            for notice in new_notices:
                print(notice)
        else:
            print("无变动")
        return
    
    # 检查是否完全相同
    if old_notices == new_notices:
        print("无变动")
        return
    
    # 找出所有变化的内容
    changed_notices = []
    
    # 比较两个列表，找出新增或变化的内容
    # 使用集合来快速检查是否存在，但保留顺序信息
    old_set = set(old_notices)
    
    # 方法：逐条比较
    # 1. 检查位置相同但内容不同的项目
    min_len = min(len(old_notices), len(new_notices))
    for i in range(min_len):
        if old_notices[i] != new_notices[i]:
            changed_notices.append(new_notices[i])
    
    # 2. 如果新列表更长，剩余部分都是新增
    if len(new_notices) > len(old_notices):
        for i in range(len(old_notices), len(new_notices)):
            changed_notices.append(new_notices[i])
    # 3. 如果旧列表更长，但新列表中有不同的内容，则整个列表都视为变化
    elif len(old_notices) > len(new_notices):
        # 检查是否有内容变化（不只是缩短）
        has_content_change = False
        for i in range(len(new_notices)):
            if old_notices[i] != new_notices[i]:
                has_content_change = True
                break
        
        # 如果旧列表更长且有内容变化，输出所有新内容
        if has_content_change:
            changed_notices = new_notices
    
    # 更新文件
    write_notices(file_path, new_notices)
    
    # 输出变化的内容
    if changed_notices:
        # 去重（相同内容只输出一次）
        unique_changes = []
        seen = set()
        for notice in changed_notices:
            if notice not in seen:
                unique_changes.append(notice)
                seen.add(notice)
        
        for notice in unique_changes:
            print(notice)
    else:
        print("无变动")

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
    notice_1 = notice_1_ + " " + url_1_  # 添加空格分隔标题和URL
    notice_2 = notice_2_ + " " + url_2_
    
    # 构建新通知列表
    new_notices = [notice_1, notice_2]
    
    # 文件路径
    file_path = os.path.join("send_notice", "notice.txt")
    
    # 获取变化并更新
    get_changes_and_update(new_notices, file_path)

if __name__ == "__main__":
    main()
