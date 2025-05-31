import datetime

def update_build(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y.%m%d.%H%M')
        if '__BUILD__' not in content:
            print(f'No __BUILD__ token found in {filepath}')
            return
        count = content.count('__BUILD__')
        new_content = content.replace('__BUILD__', timestamp, 1)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Build number updated to {timestamp}')
    except Exception as e:
        print(f'Failed to update the build number: {e}')

if __name__ == '__main__':
    update_build('devagents/hello.py')
