import requests
from lxml import etree
import os

def read_existing_notices(file_path):
    """读取已存在的通知内容"""
    try:
        print(f"尝试读取文件: {file_path}")
        print(f"文件是否存在: {os.path.exists(file_path)}")
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    print(f"读取到内容，共 {len(content.splitlines())} 行")
                    return content.split('\n')
                print("文件存在但内容为空")
                return []
        print("文件不存在")
        return []
    except FileNotFoundError:
        print("FileNotFoundError异常")
        return []
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return []

def write_notices(file_path, notices):
    """将通知写入文件"""
    try:
        # 确保目录存在
        dir_path = os.path.dirname(file_path)
        print(f"要写入的目录: {dir_path}")
        print(f"目录是否存在: {os.path.exists(dir_path)}")
        
        os.makedirs(dir_path, exist_ok=True)
        print(f"目录创建/确认完成")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(notices))
        
        print(f"成功写入文件: {file_path}")
        print(f"写入内容: {notices}")
        print(f"文件是否已创建: {os.path.exists(file_path)}")
        
    except Exception as e:
        print(f"写入文件时出错: {e}")
        raise

def get_changes_and_update(new_notices, file_path):
    """获取变化的内容并更新文件"""
    print(f"\n=== 开始检查变化 ===")
    print(f"新通知数量: {len(new_notices)}")
    for i, notice in enumerate(new_notices):
        print(f"新通知[{i}]: {notice}")
    
    old_notices = read_existing_notices(file_path)
    print(f"旧通知数量: {len(old_notices)}")
    
    # 如果没有旧内容，所有都是新的
    if not old_notices:
        print("无旧通知，创建新文件...")
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
    print("=== 脚本开始执行 ===")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"目录内容: {os.listdir('.')}")
    
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0'
    }
    
    try:
        print("\n=== 开始获取网页内容 ===")
        url_notice = "https://jw.cdu.edu.cn/"
        r_notice = requests.get(url=url_notice, headers=header, timeout=10)
        r_notice.encoding = r_notice.apparent_encoding
        print(f"请求状态码: {r_notice.status_code}")
        
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
        print(f"获取到的通知: {new_notices}")
        
        # 文件路径 - 使用跨平台兼容的路径
        file_path = os.path.join("send_notice", "notice.txt")
        print(f"文件路径: {file_path}")
        
        # 获取变化并更新
        get_changes_and_update(new_notices, file_path)
        
    except Exception as e:
        print(f"主函数执行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
    print("\n=== 脚本执行完成 ===")
