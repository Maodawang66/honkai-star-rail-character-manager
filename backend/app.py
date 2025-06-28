import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import datetime
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# 添加新的导入
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

def get_db():
    conn = sqlite3.connect('benkai.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# 用户注册
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('user_type', '玩家')
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    conn = get_db()
    try:
        conn.execute('INSERT INTO User (username, password, user_type) VALUES (?, ?, ?)',
                     (username, hash_password(password), user_type))
        conn.commit()
        return jsonify({'msg': '注册成功'})
    except sqlite3.IntegrityError:
        return jsonify({'error': '用户名已存在'}), 400
    finally:
        conn.close()

# 用户登录
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    conn = get_db()
    cur = conn.execute('SELECT * FROM User WHERE username=?', (username,))
    user = cur.fetchone()
    conn.close()
    if user and user['password'] == hash_password(password):
        return jsonify({'msg': '登录成功', 'user': {'user_id': user['user_id'], 'username': user['username'], 'user_type': user['user_type']}})
    else:
        return jsonify({'error': '用户名或密码错误'}), 400

# ========== 阵营相关API ==========
# 获取所有阵营
@app.route('/api/camps', methods=['GET'])
def get_camps():
    name = request.args.get('name')
    conn = get_db()
    if name:
        camps = conn.execute('SELECT * FROM Camp WHERE camp_name LIKE ?', (f'%{name}%',)).fetchall()
    else:
        camps = conn.execute('SELECT * FROM Camp').fetchall()
    conn.close()
    return jsonify([dict(row) for row in camps])

# 添加阵营
@app.route('/api/camps', methods=['POST'])
def add_camp():
    data = request.json
    camp_name = data.get('camp_name')
    if not camp_name:
        return jsonify({'error': '阵营名称不能为空'}), 400
    try:
        conn = get_db()
        conn.execute('INSERT INTO Camp (camp_name) VALUES (?)', (camp_name,))
        conn.commit()
        return jsonify({'msg': '添加成功'})
    except sqlite3.IntegrityError:
        return jsonify({'error': '阵营名称已存在'}), 400
    finally:
        conn.close()

# 修改阵营
@app.route('/api/camps', methods=['PUT'])
def update_camp():
    data = request.json
    old_name = data.get('old_name')
    new_name = data.get('new_name')
    if not old_name or not new_name:
        return jsonify({'error': '原名称和新名称不能为空'}), 400
    try:
        conn = get_db()
        result = conn.execute('UPDATE Camp SET camp_name=? WHERE camp_name=?', (new_name, old_name))
        if result.rowcount == 0:
            return jsonify({'error': '未找到指定的阵营'}), 404
        conn.commit()
        return jsonify({'msg': '修改成功'})
    except sqlite3.IntegrityError:
        return jsonify({'error': '新阵营名称已存在'}), 400
    finally:
        conn.close()

# 删除阵营
@app.route('/api/camps', methods=['DELETE'])
def delete_camp():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': '阵营名称不能为空'}), 400
    try:
        conn = get_db()
        result = conn.execute('DELETE FROM Camp WHERE camp_name=?', (name,))
        if result.rowcount == 0:
            return jsonify({'error': '未找到指定的阵营'}), 404
        conn.commit()
        return jsonify({'msg': '删除成功'})
    except Exception as e:
        return jsonify({'error': '删除失败，可能存在关联数据'}), 400
    finally:
        conn.close()

# ========== 属性相关API ==========
# 获取所有属性
@app.route('/api/attributes', methods=['GET'])
def get_attributes():
    name = request.args.get('name')
    conn = get_db()
    if name:
        attrs = conn.execute('SELECT * FROM Attribute WHERE attribute_name LIKE ?', (f'%{name}%',)).fetchall()
    else:
        attrs = conn.execute('SELECT * FROM Attribute').fetchall()
    conn.close()
    return jsonify([dict(row) for row in attrs])

# 添加属性
@app.route('/api/attributes', methods=['POST'])
def add_attribute():
    data = request.json
    attribute_name = data.get('attribute_name')
    if not attribute_name:
        return jsonify({'error': '属性名称不能为空'}), 400
    try:
        conn = get_db()
        conn.execute('INSERT INTO Attribute (attribute_name) VALUES (?)', (attribute_name,))
        conn.commit()
        return jsonify({'msg': '添加成功'})
    except sqlite3.IntegrityError:
        return jsonify({'error': '属性名称已存在'}), 400
    finally:
        conn.close()

# 修改属性
@app.route('/api/attributes', methods=['PUT'])
def update_attribute():
    data = request.json
    old_name = data.get('old_name')
    new_name = data.get('new_name')
    if not old_name or not new_name:
        return jsonify({'error': '原名称和新名称不能为空'}), 400
    try:
        conn = get_db()
        result = conn.execute('UPDATE Attribute SET attribute_name=? WHERE attribute_name=?', (new_name, old_name))
        if result.rowcount == 0:
            return jsonify({'error': '未找到指定的属性'}), 404
        conn.commit()
        return jsonify({'msg': '修改成功'})
    except sqlite3.IntegrityError:
        return jsonify({'error': '新属性名称已存在'}), 400
    finally:
        conn.close()

# 删除属性
@app.route('/api/attributes', methods=['DELETE'])
def delete_attribute():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': '属性名称不能为空'}), 400
    try:
        conn = get_db()
        result = conn.execute('DELETE FROM Attribute WHERE attribute_name=?', (name,))
        if result.rowcount == 0:
            return jsonify({'error': '未找到指定的属性'}), 404
        conn.commit()
        return jsonify({'msg': '删除成功'})
    except Exception as e:
        return jsonify({'error': '删除失败，可能存在关联数据'}), 400
    finally:
        conn.close()

# ========== 命途相关API ==========
# 获取所有命途
@app.route('/api/fates', methods=['GET'])
def get_fates():
    name = request.args.get('name')
    conn = get_db()
    if name:
        fates = conn.execute('SELECT * FROM Fate WHERE fate_name LIKE ?', (f'%{name}%',)).fetchall()
    else:
        fates = conn.execute('SELECT * FROM Fate').fetchall()
    conn.close()
    return jsonify([dict(row) for row in fates])

# 添加命途
@app.route('/api/fates', methods=['POST'])
def add_fate():
    data = request.json
    fate_name = data.get('fate_name')
    if not fate_name:
        return jsonify({'error': '命途名称不能为空'}), 400
    try:
        conn = get_db()
        conn.execute('INSERT INTO Fate (fate_name) VALUES (?)', (fate_name,))
        conn.commit()
        return jsonify({'msg': '添加成功'})
    except sqlite3.IntegrityError:
        return jsonify({'error': '命途名称已存在'}), 400
    finally:
        conn.close()

# 修改命途
@app.route('/api/fates', methods=['PUT'])
def update_fate():
    data = request.json
    old_name = data.get('old_name')
    new_name = data.get('new_name')
    if not old_name or not new_name:
        return jsonify({'error': '原名称和新名称不能为空'}), 400
    try:
        conn = get_db()
        result = conn.execute('UPDATE Fate SET fate_name=? WHERE fate_name=?', (new_name, old_name))
        if result.rowcount == 0:
            return jsonify({'error': '未找到指定的命途'}), 404
        conn.commit()
        return jsonify({'msg': '修改成功'})
    except sqlite3.IntegrityError:
        return jsonify({'error': '新命途名称已存在'}), 400
    finally:
        conn.close()

# 删除命途
@app.route('/api/fates', methods=['DELETE'])
def delete_fate():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': '命途名称不能为空'}), 400
    try:
        conn = get_db()
        result = conn.execute('DELETE FROM Fate WHERE fate_name=?', (name,))
        if result.rowcount == 0:
            return jsonify({'error': '未找到指定的命途'}), 404
        conn.commit()
        return jsonify({'msg': '删除成功'})
    except Exception as e:
        return jsonify({'error': '删除失败，可能存在关联数据'}), 400
    finally:
        conn.close()

# ========== 标签相关API ==========
# 获取所有标签
@app.route('/api/tags', methods=['GET'])
def get_tags():
    name = request.args.get('name')
    conn = get_db()
    if name:
        tags = conn.execute('SELECT * FROM Tag WHERE name LIKE ?', (f'%{name}%',)).fetchall()
    else:
        tags = conn.execute('SELECT * FROM Tag').fetchall()
    conn.close()
    return jsonify([dict(row) for row in tags])

# 添加标签
@app.route('/api/tags', methods=['POST'])
def add_tag():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({'error': '标签名称不能为空'}), 400
    try:
        conn = get_db()
        conn.execute('INSERT INTO Tag (name) VALUES (?)', (name,))
        conn.commit()
        return jsonify({'msg': '添加成功'})
    except sqlite3.IntegrityError:
        return jsonify({'error': '标签名称已存在'}), 400
    finally:
        conn.close()

# 修改标签
@app.route('/api/tags', methods=['PUT'])
def update_tag():
    data = request.json
    old_name = data.get('old_name')
    new_name = data.get('new_name')
    if not old_name or not new_name:
        return jsonify({'error': '原名称和新名称不能为空'}), 400
    try:
        conn = get_db()
        result = conn.execute('UPDATE Tag SET name=? WHERE name=?', (new_name, old_name))
        if result.rowcount == 0:
            return jsonify({'error': '未找到指定的标签'}), 404
        conn.commit()
        return jsonify({'msg': '修改成功'})
    except sqlite3.IntegrityError:
        return jsonify({'error': '新标签名称已存在'}), 400
    finally:
        conn.close()

# 删除标签
@app.route('/api/tags', methods=['DELETE'])
def delete_tag():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': '标签名称不能为空'}), 400
    try:
        conn = get_db()
        result = conn.execute('DELETE FROM Tag WHERE name=?', (name,))
        if result.rowcount == 0:
            return jsonify({'error': '未找到指定的标签'}), 404
        conn.commit()
        return jsonify({'msg': '删除成功'})
    except Exception as e:
        return jsonify({'error': '删除失败，可能存在关联数据'}), 400
    finally:
        conn.close()

# ========== 角色相关API ==========
# 获取所有角色（简单信息）
@app.route('/api/characters', methods=['GET'])
def get_characters():
    conn = get_db()
    chars = conn.execute('SELECT * FROM Character').fetchall()
    conn.close()
    return jsonify([dict(row) for row in chars])

# 获取角色详细信息（包含关联标签）
@app.route('/api/characters/detail', methods=['GET'])
def get_characters_detail():
    conn = get_db()
    chars = conn.execute('''
        SELECT c.*, camp.camp_name, attr.attribute_name, fate.fate_name 
        FROM Character c 
        LEFT JOIN Camp camp ON c.camp_id = camp.camp_id 
        LEFT JOIN Attribute attr ON c.attribute_id = attr.attribute_id 
        LEFT JOIN Fate fate ON c.fate_id = fate.fate_id
    ''').fetchall()
    
    result = []
    for char in chars:
        char_dict = dict(char)
        # 获取关联的标签
        tags = conn.execute('''
            SELECT t.name FROM Character_Tag ct 
            JOIN Tag t ON ct.tag_id = t.tag_id 
            WHERE ct.character_id = ?
        ''', (char['character_id'],)).fetchall()
        char_dict['tags'] = [tag['name'] for tag in tags]
        result.append(char_dict)
    
    conn.close()
    return jsonify(result)

# 获取单个角色详细信息
@app.route('/api/characters/detail/<name>', methods=['GET'])
def get_character_detail(name):
    conn = get_db()
    char = conn.execute('''
        SELECT c.*, camp.camp_name, attr.attribute_name, fate.fate_name 
        FROM Character c 
        LEFT JOIN Camp camp ON c.camp_id = camp.camp_id 
        LEFT JOIN Attribute attr ON c.attribute_id = attr.attribute_id 
        LEFT JOIN Fate fate ON c.fate_id = fate.fate_id 
        WHERE c.name = ?
    ''', (name,)).fetchone()
    
    if not char:
        return jsonify({'error': '未找到角色'}), 404
    
    char_dict = dict(char)
    # 获取关联的标签
    tags = conn.execute('''
        SELECT t.name FROM Character_Tag ct 
        JOIN Tag t ON ct.tag_id = t.tag_id 
        WHERE ct.character_id = ?
    ''', (char['character_id'],)).fetchall()
    char_dict['tags'] = [tag['name'] for tag in tags]
    
    conn.close()
    return jsonify(char_dict)

# 新增角色
@app.route('/api/characters', methods=['POST'])
def add_character():
    data = request.json
    try:
        conn = get_db()
        conn.execute('INSERT INTO Character (name, description, camp_id, attribute_id, fate_id, skill) VALUES (?, ?, ?, ?, ?, ?)',
                     (data['name'], data.get('description'), data.get('camp_id'), data.get('attribute_id'), data.get('fate_id'), data.get('skill')))
        conn.commit()
        return jsonify({'msg': '添加成功'})
    except sqlite3.IntegrityError:
        return jsonify({'error': '角色名已存在'}), 400
    finally:
        conn.close()

# 修改角色
@app.route('/api/characters', methods=['PUT'])
def update_character():
    data = request.json
    old_name = data.get('old_name')
    new_name = data.get('new_name')
    if not old_name or not new_name:
        return jsonify({'error': '原名称和新名称不能为空'}), 400
    try:
        conn = get_db()
        result = conn.execute('UPDATE Character SET name=?, description=?, camp_id=?, attribute_id=?, fate_id=?, skill=? WHERE name=?',
                     (new_name, data.get('description'), data.get('camp_id'), data.get('attribute_id'), data.get('fate_id'), data.get('skill'), old_name))
        if result.rowcount == 0:
            return jsonify({'error': '未找到指定的角色'}), 404
        conn.commit()
        return jsonify({'msg': '修改成功'})
    except sqlite3.IntegrityError:
        return jsonify({'error': '新角色名称已存在'}), 400
    finally:
        conn.close()

# 删除角色
@app.route('/api/characters', methods=['DELETE'])
def delete_character_by_name():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': '角色名称不能为空'}), 400
    try:
        conn = get_db()
        result = conn.execute('DELETE FROM Character WHERE name=?', (name,))
        if result.rowcount == 0:
            return jsonify({'error': '未找到指定的角色'}), 404
        conn.commit()
        return jsonify({'msg': '删除成功'})
    except Exception as e:
        return jsonify({'error': '删除失败，可能存在关联数据'}), 400
    finally:
        conn.close()

# ========== BOSS相关API ==========
# 获取所有BOSS（简单信息）
@app.route('/api/bosses', methods=['GET'])
def get_bosses():
    conn = get_db()
    bosses = conn.execute('SELECT * FROM Boss').fetchall()
    conn.close()
    return jsonify([dict(row) for row in bosses])

# 获取BOSS详细信息（包含关联标签）
@app.route('/api/bosses/detail', methods=['GET'])
def get_bosses_detail():
    conn = get_db()
    bosses = conn.execute('''
        SELECT b.*, camp.camp_name, attr.attribute_name as weakness_name 
        FROM Boss b 
        LEFT JOIN Camp camp ON b.camp_id = camp.camp_id 
        LEFT JOIN Attribute attr ON b.weakness_id = attr.attribute_id
    ''').fetchall()
    
    result = []
    for boss in bosses:
        boss_dict = dict(boss)
        # 获取关联的标签
        tags = conn.execute('''
            SELECT t.name FROM Boss_Tag bt 
            JOIN Tag t ON bt.tag_id = t.tag_id 
            WHERE bt.boss_id = ?
        ''', (boss['boss_id'],)).fetchall()
        boss_dict['tags'] = [tag['name'] for tag in tags]
        result.append(boss_dict)
    
    conn.close()
    return jsonify(result)

# 获取单个BOSS详细信息
@app.route('/api/bosses/detail/<name>', methods=['GET'])
def get_boss_detail(name):
    conn = get_db()
    boss = conn.execute('''
        SELECT b.*, camp.camp_name, attr.attribute_name as weakness_name 
        FROM Boss b 
        LEFT JOIN Camp camp ON b.camp_id = camp.camp_id 
        LEFT JOIN Attribute attr ON b.weakness_id = attr.attribute_id 
        WHERE b.name = ?
    ''', (name,)).fetchone()
    
    if not boss:
        return jsonify({'error': '未找到BOSS'}), 404
    
    boss_dict = dict(boss)
    # 获取关联的标签
    tags = conn.execute('''
        SELECT t.name FROM Boss_Tag bt 
        JOIN Tag t ON bt.tag_id = t.tag_id 
        WHERE bt.boss_id = ?
    ''', (boss['boss_id'],)).fetchall()
    boss_dict['tags'] = [tag['name'] for tag in tags]
    
    conn.close()
    return jsonify(boss_dict)

# 添加BOSS
@app.route('/api/bosses', methods=['POST'])
def add_boss():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({'error': 'BOSS名称不能为空'}), 400
    try:
        conn = get_db()
        conn.execute('INSERT INTO Boss (name, description, camp_id, weakness_id) VALUES (?, ?, ?, ?)',
                     (name, data.get('description'), data.get('camp_id'), data.get('weakness_id')))
        conn.commit()
        return jsonify({'msg': '添加成功'})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'BOSS名称已存在'}), 400
    finally:
        conn.close()

# 修改BOSS
@app.route('/api/bosses', methods=['PUT'])
def update_boss():
    data = request.json
    old_name = data.get('old_name')
    new_name = data.get('new_name')
    if not old_name or not new_name:
        return jsonify({'error': '原名称和新名称不能为空'}), 400
    try:
        conn = get_db()
        result = conn.execute('UPDATE Boss SET name=?, description=?, camp_id=?, weakness_id=? WHERE name=?',
                     (new_name, data.get('description'), data.get('camp_id'), data.get('weakness_id'), old_name))
        if result.rowcount == 0:
            return jsonify({'error': '未找到指定的BOSS'}), 404
        conn.commit()
        return jsonify({'msg': '修改成功'})
    except sqlite3.IntegrityError:
        return jsonify({'error': '新BOSS名称已存在'}), 400
    finally:
        conn.close()

# 删除BOSS
@app.route('/api/bosses', methods=['DELETE'])
def delete_boss():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'BOSS名称不能为空'}), 400
    try:
        conn = get_db()
        result = conn.execute('DELETE FROM Boss WHERE name=?', (name,))
        if result.rowcount == 0:
            return jsonify({'error': '未找到指定的BOSS'}), 404
        conn.commit()
        return jsonify({'msg': '删除成功'})
    except Exception as e:
        return jsonify({'error': '删除失败，可能存在关联数据'}), 400
    finally:
        conn.close()

# ========== 环境相关API ==========
# 获取所有环境（简单信息）
@app.route('/api/environments', methods=['GET'])
def get_envs():
    conn = get_db()
    envs = conn.execute('SELECT * FROM Environment').fetchall()
    conn.close()
    return jsonify([dict(row) for row in envs])

# 获取环境详细信息（包含关联标签）
@app.route('/api/environments/detail', methods=['GET'])
def get_environments_detail():
    conn = get_db()
    envs = conn.execute('SELECT * FROM Environment').fetchall()
    
    result = []
    for env in envs:
        env_dict = dict(env)
        # 获取关联的标签
        tags = conn.execute('''
            SELECT t.name FROM Environment_Tag et 
            JOIN Tag t ON et.tag_id = t.tag_id 
            WHERE et.env_id = ?
        ''', (env['env_id'],)).fetchall()
        env_dict['tags'] = [tag['name'] for tag in tags]
        result.append(env_dict)
    
    conn.close()
    return jsonify(result)

# 获取单个环境详细信息
@app.route('/api/environments/detail/<name>', methods=['GET'])
def get_environment_detail(name):
    conn = get_db()
    env = conn.execute('SELECT * FROM Environment WHERE name = ?', (name,)).fetchone()
    
    if not env:
        return jsonify({'error': '未找到环境'}), 404
    
    env_dict = dict(env)
    # 获取关联的标签
    tags = conn.execute('''
        SELECT t.name FROM Environment_Tag et 
        JOIN Tag t ON et.tag_id = t.tag_id 
        WHERE et.env_id = ?
    ''', (env['env_id'],)).fetchall()
    env_dict['tags'] = [tag['name'] for tag in tags]
    
    conn.close()
    return jsonify(env_dict)

# 添加环境
@app.route('/api/environments', methods=['POST'])
def add_environment():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({'error': '环境名称不能为空'}), 400
    try:
        conn = get_db()
        conn.execute('INSERT INTO Environment (name, buff) VALUES (?, ?)',
                     (name, data.get('buff')))
        conn.commit()
        return jsonify({'msg': '添加成功'})
    except sqlite3.IntegrityError:
        return jsonify({'error': '环境名称已存在'}), 400
    finally:
        conn.close()

# 修改环境
@app.route('/api/environments', methods=['PUT'])
def update_environment():
    data = request.json
    old_name = data.get('old_name')
    new_name = data.get('new_name')
    if not old_name or not new_name:
        return jsonify({'error': '原名称和新名称不能为空'}), 400
    try:
        conn = get_db()
        result = conn.execute('UPDATE Environment SET name=?, buff=? WHERE name=?',
                     (new_name, data.get('buff'), old_name))
        if result.rowcount == 0:
            return jsonify({'error': '未找到指定的环境'}), 404
        conn.commit()
        return jsonify({'msg': '修改成功'})
    except sqlite3.IntegrityError:
        return jsonify({'error': '新环境名称已存在'}), 400
    finally:
        conn.close()

# 删除环境
@app.route('/api/environments', methods=['DELETE'])
def delete_environment():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': '环境名称不能为空'}), 400
    try:
        conn = get_db()
        result = conn.execute('DELETE FROM Environment WHERE name=?', (name,))
        if result.rowcount == 0:
            return jsonify({'error': '未找到指定的环境'}), 404
        conn.commit()
        return jsonify({'msg': '删除成功'})
    except Exception as e:
        return jsonify({'error': '删除失败，可能存在关联数据'}), 400
    finally:
        conn.close()

# ========== 关联关系API ==========
# 角色-标签关联
@app.route('/api/character_tags', methods=['POST'])
def add_character_tag():
    data = request.json
    character_id = data.get('character_id')
    tag_id = data.get('tag_id')
    if not character_id or not tag_id:
        return jsonify({'error': '角色ID和标签ID不能为空'}), 400
    try:
        conn = get_db()
        conn.execute('INSERT INTO Character_Tag (character_id, tag_id) VALUES (?, ?)', (character_id, tag_id))
        conn.commit()
        return jsonify({'msg': '添加成功'})
    except sqlite3.IntegrityError:
        return jsonify({'error': '该关联已存在'}), 400
    finally:
        conn.close()

@app.route('/api/character_tags', methods=['DELETE'])
def delete_character_tag():
    data = request.json
    character_id = data.get('character_id')
    tag_id = data.get('tag_id')
    if not character_id or not tag_id:
        return jsonify({'error': '角色ID和标签ID不能为空'}), 400
    try:
        conn = get_db()
        result = conn.execute('DELETE FROM Character_Tag WHERE character_id=? AND tag_id=?', (character_id, tag_id))
        if result.rowcount == 0:
            return jsonify({'error': '未找到指定的关联'}), 404
        conn.commit()
        return jsonify({'msg': '删除成功'})
    except Exception as e:
        return jsonify({'error': '删除失败'}), 400
    finally:
        conn.close()

# 环境-标签关联
@app.route('/api/environment_tags', methods=['POST'])
def add_environment_tag():
    data = request.json
    env_id = data.get('env_id')
    tag_id = data.get('tag_id')
    if not env_id or not tag_id:
        return jsonify({'error': '环境ID和标签ID不能为空'}), 400
    try:
        conn = get_db()
        conn.execute('INSERT INTO Environment_Tag (env_id, tag_id) VALUES (?, ?)', (env_id, tag_id))
        conn.commit()
        return jsonify({'msg': '添加成功'})
    except sqlite3.IntegrityError:
        return jsonify({'error': '该关联已存在'}), 400
    finally:
        conn.close()

@app.route('/api/environment_tags', methods=['DELETE'])
def delete_environment_tag():
    data = request.json
    env_id = data.get('env_id')
    tag_id = data.get('tag_id')
    if not env_id or not tag_id:
        return jsonify({'error': '环境ID和标签ID不能为空'}), 400
    try:
        conn = get_db()
        result = conn.execute('DELETE FROM Environment_Tag WHERE env_id=? AND tag_id=?', (env_id, tag_id))
        if result.rowcount == 0:
            return jsonify({'error': '未找到指定的关联'}), 404
        conn.commit()
        return jsonify({'msg': '删除成功'})
    except Exception as e:
        return jsonify({'error': '删除失败'}), 400
    finally:
        conn.close()

# BOSS-标签关联
@app.route('/api/boss_tags', methods=['POST'])
def add_boss_tag():
    data = request.json
    boss_id = data.get('boss_id')
    tag_id = data.get('tag_id')
    if not boss_id or not tag_id:
        return jsonify({'error': 'BOSS ID和标签ID不能为空'}), 400
    try:
        conn = get_db()
        conn.execute('INSERT INTO Boss_Tag (boss_id, tag_id) VALUES (?, ?)', (boss_id, tag_id))
        conn.commit()
        return jsonify({'msg': '添加成功'})
    except sqlite3.IntegrityError:
        return jsonify({'error': '该关联已存在'}), 400
    finally:
        conn.close()

@app.route('/api/boss_tags', methods=['DELETE'])
def delete_boss_tag():
    data = request.json
    boss_id = data.get('boss_id')
    tag_id = data.get('tag_id')
    if not boss_id or not tag_id:
        return jsonify({'error': 'BOSS ID和标签ID不能为空'}), 400
    try:
        conn = get_db()
        result = conn.execute('DELETE FROM Boss_Tag WHERE boss_id=? AND tag_id=?', (boss_id, tag_id))
        if result.rowcount == 0:
            return jsonify({'error': '未找到指定的关联'}), 404
        conn.commit()
        return jsonify({'msg': '删除成功'})
    except Exception as e:
        return jsonify({'error': '删除失败'}), 400
    finally:
        conn.close()

# ========== 用户相关API ==========
# 用户-角色相关
@app.route('/api/user_characters/<int:user_id>', methods=['GET'])
def get_user_characters(user_id):
    conn = get_db()
    sql = '''SELECT uc.*, c.name FROM User_Character uc JOIN Character c ON uc.character_id = c.character_id WHERE uc.user_id=?'''
    rows = conn.execute(sql, (user_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# 获取特定用户的特定角色信息
@app.route('/api/user_characters/<int:user_id>/<int:character_id>', methods=['GET'])
def get_user_character(user_id, character_id):
    try:
        conn = get_db()
        sql = '''SELECT uc.*, c.name FROM User_Character uc 
                 JOIN Character c ON uc.character_id = c.character_id 
                 WHERE uc.user_id=? AND uc.character_id=?'''
        row = conn.execute(sql, (user_id, character_id)).fetchone()
        conn.close()
        
        if row:
            return jsonify(dict(row))
        else:
            return jsonify({'error': '未找到该角色'}), 404
    except Exception as e:
        return jsonify({'error': f'查询失败: {str(e)}'}), 500

# 添加用户角色
@app.route('/api/user_characters', methods=['POST'])
def add_user_character():
    try:
        data = request.json
        user_id = data.get('user_id')
        character_id = data.get('character_id')
        star_soul = data.get('star_soul', 0)
        level = data.get('level', 1)
        favor = data.get('favor', 5)
        join_time = data.get('join_time')
        
        if not user_id or not character_id:
            return jsonify({'error': '用户ID和角色ID不能为空'}), 400
        
        # 验证数值范围
        if not (0 <= star_soul <= 6):
            return jsonify({'error': '星魂必须在0-6之间'}), 400
        if not (1 <= level <= 80):
            return jsonify({'error': '等级必须在1-80之间'}), 400
        if not (0 <= favor <= 10):
            return jsonify({'error': '好感度必须在0-10之间'}), 400
        
        # 计算战力：战力 = 等级 * (1 + 星魂 * 15%)
        power = int(level * (1 + star_soul * 0.15))
        
        conn = get_db()
        
        # 检查角色是否已存在
        existing = conn.execute('SELECT user_id FROM User_Character WHERE user_id=? AND character_id=?', 
                               (user_id, character_id)).fetchone()
        if existing:
            conn.close()
            return jsonify({'error': '该角色已存在，请使用修改功能'}), 400
        
        # 插入新角色
        conn.execute('''INSERT INTO User_Character 
                       (user_id, character_id, star_soul, level, power, join_time, favor) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (user_id, character_id, star_soul, level, power, join_time, favor))
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': '角色添加成功',
            'power': power
        })
        
    except sqlite3.IntegrityError as e:
        return jsonify({'error': '数据完整性错误'}), 400
    except Exception as e:
        return jsonify({'error': f'添加失败: {str(e)}'}), 500

# 修改用户角色
@app.route('/api/user_characters', methods=['PUT'])
def update_user_character():
    try:
        data = request.json
        logging.debug(f'Received data for update: {data}')
        user_id = data.get('user_id')
        character_id = data.get('character_id')
        star_soul = data.get('star_soul')
        level = data.get('level')
        favor = data.get('favor')
        power = data.get('power')
        
        if not user_id or not character_id:
            logging.error('User ID or Character ID is missing')
            return jsonify({'error': '用户ID和角色ID不能为空'}), 400
        
        conn = get_db()
        
        # 检查角色是否存在
        existing = conn.execute('SELECT * FROM User_Character WHERE user_id=? AND character_id=?', 
                               (user_id, character_id)).fetchone()
        if not existing:
            logging.error('Character does not exist')
            conn.close()
            return jsonify({'error': '该角色不存在'}), 404
        
        # 构建更新SQL和参数
        update_fields = []
        params = []
        
        if star_soul is not None:
            if not (0 <= star_soul <= 6):
                logging.error('Star soul out of range')
                return jsonify({'error': '星魂必须在0-6之间'}), 400
            update_fields.append('star_soul = ?')
            params.append(star_soul)
        else:
            star_soul = existing['star_soul']
            
        if level is not None:
            if not (1 <= level <= 80):
                logging.error('Level out of range')
                return jsonify({'error': '等级必须在1-80之间'}), 400
            update_fields.append('level = ?')
            params.append(level)
        else:
            level = existing['level']
            
        if favor is not None:
            if not (0 <= favor <= 10):
                logging.error('Favor out of range')
                return jsonify({'error': '好感度必须在0-10之间'}), 400
            update_fields.append('favor = ?')
            params.append(favor)
            
        if power is not None:
            update_fields.append('power = ?')
            params.append(power)
        else:
            # 重新计算战力
            power = int(level * (1 + star_soul * 0.15))
            update_fields.append('power = ?')
            params.append(power)
        
        # 添加WHERE条件参数
        params.extend([user_id, character_id])
        
        if update_fields:
            sql = f"UPDATE User_Character SET {', '.join(update_fields)} WHERE user_id = ? AND character_id = ?"
            logging.debug(f'Executing SQL: {sql} with params: {params}')
            conn.execute(sql, params)
            conn.commit()
            logging.info('Character updated successfully')
        
        conn.close()
        
        return jsonify({
            'message': '角色修改成功',
            'power': power
        })
        
    except Exception as e:
        logging.error(f'Update failed: {str(e)}')
        return jsonify({'error': f'修改失败: {str(e)}'}), 500

# 删除用户角色
@app.route('/api/user_characters/<int:user_id>/<int:character_id>', methods=['DELETE'])
def delete_user_character(user_id, character_id):
    try:
        conn = get_db()
        
        # 检查角色是否存在
        existing = conn.execute('SELECT user_id FROM User_Character WHERE user_id=? AND character_id=?', 
                               (user_id, character_id)).fetchone()
        if not existing:
            conn.close()
            return jsonify({'error': '该角色不存在'}), 404
        
        # 删除角色
        result = conn.execute('DELETE FROM User_Character WHERE user_id=? AND character_id=?', 
                             (user_id, character_id))
        
        if result.rowcount > 0:
            conn.commit()
            conn.close()
            return jsonify({'message': '角色删除成功'})
        else:
            conn.close()
            return jsonify({'error': '删除失败'}), 400
            
    except Exception as e:
        return jsonify({'error': f'删除失败: {str(e)}'}), 500

# ========== 统计相关API ==========
# 统计接口示例
@app.route('/api/stat/character_power_rank', methods=['GET'])
def stat_character_power_rank():
    user_id = request.args.get('user_id')
    name = request.args.get('name')
    conn = get_db()
    sql = '''SELECT c.name, AVG(uc.power) as avg_power FROM User_Character uc JOIN Character c ON uc.character_id = c.character_id'''
    params = []
    where = []
    if user_id:
        where.append('uc.user_id=?')
        params.append(user_id)
    if name:
        where.append('c.name LIKE ?')
        params.append(f'%{name}%')
    if where:
        sql += ' WHERE ' + ' AND '.join(where)
    sql += ' GROUP BY c.character_id ORDER BY avg_power DESC LIMIT 20'
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return jsonify([{'name': row['name'], 'avg_power': row['avg_power']} for row in rows])

@app.route('/api/stat/character_hold_rate', methods=['GET'])
def stat_character_hold_rate():
    user_id = request.args.get('user_id')
    name = request.args.get('name')
    conn = get_db()
    sql = '''SELECT c.name, COUNT(uc.user_id) as user_count, (COUNT(uc.user_id)*1.0/(SELECT COUNT(*) FROM User)) as hold_rate FROM Character c LEFT JOIN User_Character uc ON c.character_id = uc.character_id'''
    params = []
    where = []
    if user_id:
        where.append('uc.user_id=?')
        params.append(user_id)
    if name:
        where.append('c.name LIKE ?')
        params.append(f'%{name}%')
    if where:
        sql += ' WHERE ' + ' AND '.join(where)
    sql += ' GROUP BY c.character_id ORDER BY hold_rate DESC LIMIT 20'
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return jsonify([{'name': row['name'], 'user_count': row['user_count'], 'hold_rate': row['hold_rate']} for row in rows])

# ========== 新增战力排行和角色持有率API ==========
# 查询指定角色的战力排行
@app.route('/api/power-ranking/character/<character_name>', methods=['GET'])
def get_character_power_ranking(character_name):
    try:
        conn = get_db()
        sql = '''
        SELECT u.username, c.name as character_name, uc.power as power_value
        FROM User_Character uc 
        JOIN User u ON uc.user_id = u.user_id 
        JOIN Character c ON uc.character_id = c.character_id 
        WHERE c.name = ?
        ORDER BY uc.power DESC
        '''
        rows = conn.execute(sql, (character_name,)).fetchall()
        conn.close()
        
        if not rows:
            return jsonify({'error': f'未找到角色 {character_name} 的战力数据'}), 404
        
        result = []
        for row in rows:
            result.append({
                'username': row['username'],
                'character_name': row['character_name'],
                'power_value': row['power_value']
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'查询失败: {str(e)}'}), 500

# 查询全服所有角色的战力排行
@app.route('/api/power-ranking/all', methods=['GET'])
def get_all_power_ranking():
    try:
        conn = get_db()
        sql = '''
        SELECT u.username, c.name as character_name, uc.power as power_value
        FROM User_Character uc 
        JOIN User u ON uc.user_id = u.user_id 
        JOIN Character c ON uc.character_id = c.character_id 
        ORDER BY uc.power DESC
        '''
        rows = conn.execute(sql).fetchall()
        conn.close()
        
        result = []
        for row in rows:
            result.append({
                'username': row['username'],
                'character_name': row['character_name'],
                'power_value': row['power_value']
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'查询失败: {str(e)}'}), 500

# 查询角色持有率
@app.route('/api/character-ownership/<character_name>', methods=['GET'])
def get_character_ownership(character_name):
    try:
        conn = get_db()
        
        # 检查角色是否存在
        character_check = conn.execute('SELECT character_id FROM Character WHERE name = ?', (character_name,)).fetchone()
        if not character_check:
            return jsonify({'error': f'角色 {character_name} 不存在'}), 404
        
        character_id = character_check['character_id']
        
        # 查询拥有该角色的玩家数量
        owners_sql = '''
        SELECT COUNT(DISTINCT user_id) as owners 
        FROM User_Character 
        WHERE character_id = ?
        '''
        owners_result = conn.execute(owners_sql, (character_id,)).fetchone()
        owners_count = owners_result['owners']
        
        # 查询总玩家数量
        total_players_sql = 'SELECT COUNT(*) as total FROM User'
        total_result = conn.execute(total_players_sql).fetchone()
        total_players = total_result['total']
        
        conn.close()
        
        if total_players == 0:
            return jsonify({'error': '系统中暂无玩家数据'}), 404
        
        result = {
            'character_name': character_name,
            'owners': owners_count,
            'total_players': total_players,
            'ownership_rate': round((owners_count / total_players) * 100, 2)
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'查询失败: {str(e)}'}), 500

# ========== 阵容推荐API ==========
# 基于BOSS的角色推荐
@app.route('/api/recommendations/boss/<int:boss_id>/<int:user_id>', methods=['GET'])
def recommend_characters_for_boss(boss_id, user_id):
    try:
        conn = get_db()
        
        # 获取BOSS的标签
        boss_tags_sql = '''
            SELECT t.tag_id, t.name 
            FROM Boss_Tag bt 
            JOIN Tag t ON bt.tag_id = t.tag_id 
            WHERE bt.boss_id = ?
        '''
        boss_tags = conn.execute(boss_tags_sql, (boss_id,)).fetchall()
        boss_tag_ids = [tag['tag_id'] for tag in boss_tags]
        
        # 获取用户拥有的角色及其详细信息
        user_chars_sql = '''
            SELECT uc.*, c.name as character_name,
                   GROUP_CONCAT(t.name) as character_tags
            FROM User_Character uc
            JOIN Character c ON uc.character_id = c.character_id
            LEFT JOIN Character_Tag ct ON c.character_id = ct.character_id
            LEFT JOIN Tag t ON ct.tag_id = t.tag_id
            WHERE uc.user_id = ?
            GROUP BY uc.character_id
        '''
        user_characters = conn.execute(user_chars_sql, (user_id,)).fetchall()
        
        recommendations = []
        
        for char in user_characters:
            # 获取角色的标签ID列表
            char_tags_sql = '''
                SELECT ct.tag_id 
                FROM Character_Tag ct 
                WHERE ct.character_id = ?
            '''
            char_tag_ids = [row['tag_id'] for row in conn.execute(char_tags_sql, (char['character_id'],)).fetchall()]
            
            # 计算匹配的标签数量
            matched_tags = len(set(boss_tag_ids).intersection(set(char_tag_ids)))
            
            # 计算角色优先度：战力 * (1 + 好感度 * 0.1) * (1 + 匹配标签数 * 0.3)
            priority = char['power'] * (1 + char['favor'] * 0.1) * (1 + matched_tags * 0.3)
            
            # 获取角色标签名称列表
            char_tags_names = char['character_tags'].split(',') if char['character_tags'] else []
            
            recommendations.append({
                'character_id': char['character_id'],
                'character_name': char['character_name'],
                'star_soul': char['star_soul'],
                'level': char['level'],
                'power': char['power'],
                'favor': char['favor'],
                'join_time': char['join_time'],
                'matched_tags': matched_tags,
                'character_tags': char_tags_names,
                'priority': priority
            })
        
        # 按优先度排序，取前5个
        recommendations.sort(key=lambda x: x['priority'], reverse=True)
        top_recommendations = recommendations[:5]
        
        conn.close()
        return jsonify(top_recommendations)
        
    except Exception as e:
        return jsonify({'error': f'推荐失败: {str(e)}'}), 500

# 基于环境的角色推荐
@app.route('/api/recommendations/environment/<int:env_id>/<int:user_id>', methods=['GET'])
def recommend_characters_for_environment(env_id, user_id):
    try:
        conn = get_db()
        
        # 获取环境的标签
        env_tags_sql = '''
            SELECT t.tag_id, t.name 
            FROM Environment_Tag et 
            JOIN Tag t ON et.tag_id = t.tag_id 
            WHERE et.env_id = ?
        '''
        env_tags = conn.execute(env_tags_sql, (env_id,)).fetchall()
        env_tag_ids = [tag['tag_id'] for tag in env_tags]
        
        # 获取用户拥有的角色及其详细信息
        user_chars_sql = '''
            SELECT uc.*, c.name as character_name,
                   GROUP_CONCAT(t.name) as character_tags
            FROM User_Character uc
            JOIN Character c ON uc.character_id = c.character_id
            LEFT JOIN Character_Tag ct ON c.character_id = ct.character_id
            LEFT JOIN Tag t ON ct.tag_id = t.tag_id
            WHERE uc.user_id = ?
            GROUP BY uc.character_id
        '''
        user_characters = conn.execute(user_chars_sql, (user_id,)).fetchall()
        
        recommendations = []
        
        for char in user_characters:
            # 获取角色的标签ID列表
            char_tags_sql = '''
                SELECT ct.tag_id 
                FROM Character_Tag ct 
                WHERE ct.character_id = ?
            '''
            char_tag_ids = [row['tag_id'] for row in conn.execute(char_tags_sql, (char['character_id'],)).fetchall()]
            
            # 计算匹配的标签数量
            matched_tags = len(set(env_tag_ids).intersection(set(char_tag_ids)))
            
            # 计算角色优先度：战力 * (1 + 好感度 * 0.1) * (1 + 匹配标签数 * 0.3)
            priority = char['power'] * (1 + char['favor'] * 0.1) * (1 + matched_tags * 0.3)
            
            # 获取角色标签名称列表
            char_tags_names = char['character_tags'].split(',') if char['character_tags'] else []
            
            recommendations.append({
                'character_id': char['character_id'],
                'character_name': char['character_name'],
                'star_soul': char['star_soul'],
                'level': char['level'],
                'power': char['power'],
                'favor': char['favor'],
                'join_time': char['join_time'],
                'matched_tags': matched_tags,
                'character_tags': char_tags_names,
                'priority': priority
            })
        
        # 按优先度排序，取前5个
        recommendations.sort(key=lambda x: x['priority'], reverse=True)
        top_recommendations = recommendations[:5]
        
        conn.close()
        return jsonify(top_recommendations)
        
    except Exception as e:
        return jsonify({'error': f'推荐失败: {str(e)}'}), 500

# 综合BOSS和环境的角色推荐
@app.route('/api/recommendations/combined/<int:boss_id>/<int:env_id>/<int:user_id>', methods=['GET'])
def recommend_characters_combined(boss_id, env_id, user_id):
    try:
        conn = get_db()
        
        # 获取BOSS的标签
        boss_tags_sql = '''
            SELECT t.tag_id, t.name 
            FROM Boss_Tag bt 
            JOIN Tag t ON bt.tag_id = t.tag_id 
            WHERE bt.boss_id = ?
        '''
        boss_tags = conn.execute(boss_tags_sql, (boss_id,)).fetchall()
        boss_tag_ids = [tag['tag_id'] for tag in boss_tags]
        
        # 获取环境的标签
        env_tags_sql = '''
            SELECT t.tag_id, t.name 
            FROM Environment_Tag et 
            JOIN Tag t ON et.tag_id = t.tag_id 
            WHERE et.env_id = ?
        '''
        env_tags = conn.execute(env_tags_sql, (env_id,)).fetchall()
        env_tag_ids = [tag['tag_id'] for tag in env_tags]
        
        # 合并BOSS和环境的标签（取并集）
        combined_tag_ids = list(set(boss_tag_ids + env_tag_ids))
        
        # 获取用户拥有的角色及其详细信息
        user_chars_sql = '''
            SELECT uc.*, c.name as character_name,
                   GROUP_CONCAT(t.name) as character_tags
            FROM User_Character uc
            JOIN Character c ON uc.character_id = c.character_id
            LEFT JOIN Character_Tag ct ON c.character_id = ct.character_id
            LEFT JOIN Tag t ON ct.tag_id = t.tag_id
            WHERE uc.user_id = ?
            GROUP BY uc.character_id
        '''
        user_characters = conn.execute(user_chars_sql, (user_id,)).fetchall()
        
        recommendations = []
        
        for char in user_characters:
            # 获取角色的标签ID列表
            char_tags_sql = '''
                SELECT ct.tag_id 
                FROM Character_Tag ct 
                WHERE ct.character_id = ?
            '''
            char_tag_ids = [row['tag_id'] for row in conn.execute(char_tags_sql, (char['character_id'],)).fetchall()]
            
            # 计算与BOSS标签的匹配数量
            boss_matched_tags = len(set(boss_tag_ids).intersection(set(char_tag_ids)))
            
            # 计算与环境标签的匹配数量
            env_matched_tags = len(set(env_tag_ids).intersection(set(char_tag_ids)))
            
            # 计算与综合标签的总匹配数量
            total_matched_tags = len(set(combined_tag_ids).intersection(set(char_tag_ids)))
            
            # 计算角色优先度：战力 * (1 + 好感度 * 0.1) * (1 + 总匹配标签数 * 0.3)
            priority = char['power'] * (1 + char['favor'] * 0.1) * (1 + total_matched_tags * 0.3)
            
            # 获取角色标签名称列表
            char_tags_names = char['character_tags'].split(',') if char['character_tags'] else []
            
            recommendations.append({
                'character_id': char['character_id'],
                'character_name': char['character_name'],
                'star_soul': char['star_soul'],
                'level': char['level'],
                'power': char['power'],
                'favor': char['favor'],
                'join_time': char['join_time'],
                'matched_tags': total_matched_tags,
                'boss_matched_tags': boss_matched_tags,
                'env_matched_tags': env_matched_tags,
                'character_tags': char_tags_names,
                'priority': priority
            })
        
        # 按优先度排序，取前5个
        recommendations.sort(key=lambda x: x['priority'], reverse=True)
        top_recommendations = recommendations[:5]
        
        conn.close()
        return jsonify(top_recommendations)
        
    except Exception as e:
        return jsonify({'error': f'推荐失败: {str(e)}'}), 500

# ========== 智能分析API ==========
@app.route('/api/intelligent-analysis', methods=['GET'])
def intelligent_analysis():
    try:
        conn = get_db()
        
        # 1. 分析属性-命途组合分布
        distribution_analysis = analyze_attribute_fate_distribution(conn)
        
        # 2. 机器学习分析
        ml_analysis = perform_ml_analysis(conn)
        
        # 3. 综合推荐
        final_recommendation = generate_final_recommendation(distribution_analysis, ml_analysis, conn)
        
        conn.close()
        
        return jsonify({
            'distribution_analysis': distribution_analysis,
            'ml_analysis': ml_analysis,
            'final_recommendation': final_recommendation
        })
        
    except Exception as e:
        return jsonify({'error': f'智能分析失败: {str(e)}'}), 500

def analyze_attribute_fate_distribution(conn):
    """分析属性-命途组合的分布情况"""
    
    # 获取所有属性和命途
    attributes = conn.execute('SELECT * FROM Attribute').fetchall()
    fates = conn.execute('SELECT * FROM Fate').fetchall()
    
    # 计算每种组合的角色数量
    combinations = []
    for attr in attributes:
        for fate in fates:
            count_sql = '''
                SELECT COUNT(*) as count 
                FROM Character 
                WHERE attribute_id = ? AND fate_id = ?
            '''
            count_result = conn.execute(count_sql, (attr['attribute_id'], fate['fate_id'])).fetchone()
            combinations.append({
                'attribute_id': attr['attribute_id'],
                'attribute_name': attr['attribute_name'],
                'fate_id': fate['fate_id'],
                'fate_name': fate['fate_name'],
                'count': count_result['count']
            })
    
    # 排序找出数量最少和最多的组合
    combinations.sort(key=lambda x: x['count'])
    
    total_characters = conn.execute('SELECT COUNT(*) as count FROM Character').fetchone()['count']
    total_combinations = len(combinations)
    empty_combinations = len([c for c in combinations if c['count'] == 0])
    
    # 推荐数量少的组合（前5个）
    least_used = combinations[:5]
    
    # 避免数量多的组合（后5个）
    most_used = combinations[-5:]
    
    return {
        'total_characters': total_characters,
        'total_combinations': total_combinations,
        'empty_combinations': empty_combinations,
        'least_used': least_used,
        'most_used': most_used
    }

def perform_ml_analysis(conn):
    """使用SVR进行机器学习分析"""
    
    try:
        # 获取角色数据和相关统计
        character_data_sql = '''
            SELECT 
                c.character_id,
                c.name,
                a.attribute_name,
                f.fate_name,
                camp.camp_name,
                COUNT(uc.user_id) as ownership_count,
                COALESCE(AVG(uc.favor), 0) as avg_favor,
                (SELECT COUNT(*) FROM User) as total_users
            FROM Character c
            LEFT JOIN Attribute a ON c.attribute_id = a.attribute_id
            LEFT JOIN Fate f ON c.fate_id = f.fate_id
            LEFT JOIN Camp camp ON c.camp_id = camp.camp_id
            LEFT JOIN User_Character uc ON c.character_id = uc.character_id
            GROUP BY c.character_id
        '''
        
        character_data = conn.execute(character_data_sql).fetchall()
        
        if len(character_data) == 0:
            return {'error': '没有足够的角色数据进行分析'}
        
        # 转换为DataFrame
        df = pd.DataFrame([dict(row) for row in character_data])
        
        # 计算持有率
        df['ownership_rate'] = df['ownership_count'] / df['total_users'].fillna(1)
        
        # 处理缺失值
        df['avg_favor'] = df['avg_favor'].fillna(5.0)  # 默认好感度为5
        df['ownership_rate'] = df['ownership_rate'].fillna(0.0)
        
        # 如果数据量太少，返回简单分析
        if len(df) < 5:
            return {
                'warning': '数据量不足，无法进行有效的机器学习分析',
                'data_count': len(df)
            }
        
        # 编码分类变量
        le_attr = LabelEncoder()
        le_fate = LabelEncoder()
        le_camp = LabelEncoder()
        
        df['attribute_encoded'] = le_attr.fit_transform(df['attribute_name'].fillna('未知'))
        df['fate_encoded'] = le_fate.fit_transform(df['fate_name'].fillna('未知'))
        df['camp_encoded'] = le_camp.fit_transform(df['camp_name'].fillna('未知'))
        
        # 准备特征
        features = ['attribute_encoded', 'fate_encoded', 'camp_encoded']
        X = df[features]
        
        # 创建特征缩放器
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # 分析持有率
        y_ownership = df['ownership_rate']
        ownership_model = None
        ownership_score = 0
        
        if len(X) >= 3 and y_ownership.std() > 0:
            try:
                # 使用SVR模型
                ownership_model = SVR(
                    kernel='rbf',
                    C=1.0,
                    epsilon=0.1
                )
                
                # 使用交叉验证评估模型
                ownership_scores = cross_val_score(
                    ownership_model, X_scaled, y_ownership,
                    cv=5, scoring='r2'
                )
                ownership_score = np.mean(ownership_scores)
                
                # 训练最终模型
                ownership_model.fit(X_scaled, y_ownership)
            except:
                ownership_score = 0
        
        # 分析好感度
        y_favor = df['avg_favor']
        favor_model = None
        favor_score = 0
        
        if len(X) >= 3 and y_favor.std() > 0:
            try:
                # 使用SVR模型
                favor_model = SVR(
                    kernel='rbf',
                    C=1.0,
                    epsilon=0.1
                )
                
                # 使用交叉验证评估模型
                favor_scores = cross_val_score(
                    favor_model, X_scaled, y_favor,
                    cv=5, scoring='r2'
                )
                favor_score = np.mean(favor_scores)
                
                # 训练最终模型
                favor_model.fit(X_scaled, y_favor)
            except:
                favor_score = 0
        
        # 特征重要性分析
        feature_importance = []
        if ownership_model is not None:
            # SVR不直接提供特征重要性，我们使用基于排列的特征重要性
            from sklearn.inspection import permutation_importance
            importance = permutation_importance(
                ownership_model, X_scaled, y_ownership,
                n_repeats=10, random_state=42
            ).importances_mean
            
            feature_names = ['属性', '命途', '阵营']
            for i, imp in enumerate(importance):
                feature_importance.append({
                    'feature': feature_names[i],
                    'importance': float(imp)
                })
            feature_importance.sort(key=lambda x: x['importance'], reverse=True)
        
        return {
            'ownership_model': {
                'score': max(0, ownership_score),
                'available': ownership_model is not None
            },
            'favor_model': {
                'score': max(0, favor_score),
                'available': favor_model is not None
            },
            'feature_importance': feature_importance,
            'data_summary': {
                'total_characters': len(df),
                'avg_ownership_rate': float(df['ownership_rate'].mean()),
                'avg_favor': float(df['avg_favor'].mean())
            },
            'encoders': {
                'attributes': list(le_attr.classes_),
                'fates': list(le_fate.classes_),
                'camps': list(le_camp.classes_)
            }
        }
        
    except Exception as e:
        return {'error': f'机器学习分析失败: {str(e)}'}

def generate_final_recommendation(distribution_analysis, ml_analysis, conn):
    """生成最终的综合推荐"""
    
    try:
        # 基于分布分析的推荐
        if distribution_analysis.get('least_used'):
            recommended_combo = distribution_analysis['least_used'][0]
            recommended_attribute = recommended_combo['attribute_name']
            recommended_fate = recommended_combo['fate_name']
        else:
            # 如果没有分布数据，随机选择
            attrs = conn.execute('SELECT attribute_name FROM Attribute LIMIT 1').fetchone()
            fates = conn.execute('SELECT fate_name FROM Fate LIMIT 1').fetchone()
            recommended_attribute = attrs['attribute_name'] if attrs else '火'
            recommended_fate = fates['fate_name'] if fates else '毁灭'
        
        # 推荐阵营（选择角色数量较少的阵营）
        camp_sql = '''
            SELECT camp.camp_name, COUNT(c.character_id) as count
            FROM Camp camp
            LEFT JOIN Character c ON camp.camp_id = c.camp_id
            GROUP BY camp.camp_id
            ORDER BY count ASC
            LIMIT 1
        '''
        camp_result = conn.execute(camp_sql).fetchone()
        recommended_camp = camp_result['camp_name'] if camp_result else '星穹列车'
        
        # 生成推荐理由
        reasoning_parts = []
        
        if distribution_analysis.get('least_used'):
            combo = distribution_analysis['least_used'][0]
            reasoning_parts.append(f"{recommended_attribute}+{recommended_fate}组合当前只有{combo['count']}个角色，存在设计空间")
        
        if ml_analysis.get('feature_importance'):
            top_feature = ml_analysis['feature_importance'][0]
            reasoning_parts.append(f"机器学习分析显示{top_feature['feature']}是影响角色受欢迎程度的最重要因素")
        
        reasoning = "；".join(reasoning_parts) if reasoning_parts else "基于当前数据分布和机器学习分析的综合推荐"
        
        # 预测指标（如果有可用的模型）
        predicted_metrics = {}
        if ml_analysis.get('data_summary'):
            # 基于历史平均值给出预期
            predicted_metrics = {
                'ownership_rate': max(0.1, ml_analysis['data_summary'].get('avg_ownership_rate', 0.3)),
                'avg_favor': max(5.0, ml_analysis['data_summary'].get('avg_favor', 6.5))
            }
        
        return {
            'recommended_attribute': recommended_attribute,
            'recommended_fate': recommended_fate,
            'recommended_camp': recommended_camp,
            'reasoning': reasoning,
            'predicted_metrics': predicted_metrics
        }
        
    except Exception as e:
        return {'error': f'生成推荐失败: {str(e)}'}

# 角色推荐API
@app.route('/api/character-recommendation/<int:user_id>', methods=['GET'])
def get_character_recommendation(user_id):
    try:
        conn = get_db()
        
        # 1. 获取玩家拥有的角色信息
        user_characters_query = '''
        SELECT 
            c.character_id, c.name, c.camp_id, c.attribute_id, c.fate_id,
            uc.favor, camp.camp_name, attr.attribute_name, fate.fate_name
        FROM User_Character uc
        JOIN Character c ON uc.character_id = c.character_id
        JOIN Camp camp ON c.camp_id = camp.camp_id
        JOIN Attribute attr ON c.attribute_id = attr.attribute_id
        JOIN Fate fate ON c.fate_id = fate.fate_id
        WHERE uc.user_id = ?
        '''
        user_characters = conn.execute(user_characters_query, (user_id,)).fetchall()
        
        if len(user_characters) == 0:
            return jsonify({'error': '用户暂无角色数据，无法进行推荐'}), 400
            
        # 2. 获取玩家拥有的标签
        user_tags_query = '''
        SELECT DISTINCT t.tag_id, t.name
        FROM User_Character uc
        JOIN Character_Tag ct ON uc.character_id = ct.character_id
        JOIN Tag t ON ct.tag_id = t.tag_id
        WHERE uc.user_id = ?
        '''
        user_tags = conn.execute(user_tags_query, (user_id,)).fetchall()
        user_tag_ids = [tag['tag_id'] for tag in user_tags]
        
        # 3. 获取玩家拥有的阵营、属性、命途
        user_camps = set([char['camp_id'] for char in user_characters])
        user_attributes = set([char['attribute_id'] for char in user_characters])
        user_fates = set([char['fate_id'] for char in user_characters])
        user_attr_fate_combinations = set([(char['attribute_id'], char['fate_id']) for char in user_characters])
        user_character_ids = set([char['character_id'] for char in user_characters])
        
        # 4. 获取所有角色信息（排除玩家已拥有的）
        all_characters_query = '''
        SELECT 
            c.character_id, c.name, c.camp_id, c.attribute_id, c.fate_id,
            camp.camp_name, attr.attribute_name, fate.fate_name
        FROM Character c
        JOIN Camp camp ON c.camp_id = camp.camp_id
        JOIN Attribute attr ON c.attribute_id = attr.attribute_id
        JOIN Fate fate ON c.fate_id = fate.fate_id
        WHERE c.character_id NOT IN ({})
        '''.format(','.join(['?'] * len(user_character_ids)))
        
        all_characters = conn.execute(all_characters_query, list(user_character_ids)).fetchall()
        
        # 5. 获取每个角色的标签
        character_tags_query = '''
        SELECT ct.character_id, t.tag_id, t.name as tag_name
        FROM Character_Tag ct
        JOIN Tag t ON ct.tag_id = t.tag_id
        '''
        character_tags_result = conn.execute(character_tags_query).fetchall()
        character_tags_dict = {}
        for row in character_tags_result:
            if row['character_id'] not in character_tags_dict:
                character_tags_dict[row['character_id']] = []
            character_tags_dict[row['character_id']].append({
                'tag_id': row['tag_id'],
                'tag_name': row['tag_name']
            })
        
        # 推荐算法1: 缺失标签推荐
        missing_tags_recommendations = get_missing_tags_recommendations(
            all_characters, character_tags_dict, user_tag_ids)
        
        # 推荐算法2: 缺失阵营推荐
        missing_camps_recommendations = get_missing_camps_recommendations(
            all_characters, character_tags_dict, user_camps)
        
        # 推荐算法3: 缺失属性-命途组合推荐
        missing_combinations_recommendations = get_missing_combinations_recommendations(
            all_characters, character_tags_dict, user_attr_fate_combinations)
        
        # 推荐算法4: 高持有率推荐
        high_ownership_recommendations = get_high_ownership_recommendations(
            conn, all_characters, character_tags_dict)
        
        # 推荐算法5: 机器学习预测高好感度推荐
        predicted_high_favor_recommendations = get_ml_favor_predictions(
            conn, user_id, all_characters, character_tags_dict, user_characters)
        
        conn.close()
        
        return jsonify({
            'missing_tags_recommendations': missing_tags_recommendations[:5],
            'missing_camps_recommendations': missing_camps_recommendations[:3],
            'missing_combinations_recommendations': missing_combinations_recommendations[:3],
            'high_ownership_recommendations': high_ownership_recommendations[:5],
            'predicted_high_favor_recommendations': predicted_high_favor_recommendations[:5]
        })
        
    except Exception as e:
        return jsonify({'error': f'推荐失败: {str(e)}'}), 500

def get_missing_tags_recommendations(all_characters, character_tags_dict, user_tag_ids):
    """推荐可以补充缺失标签的角色"""
    recommendations = []
    
    for char in all_characters:
        char_id = char['character_id']
        char_tags = character_tags_dict.get(char_id, [])
        char_tag_ids = [tag['tag_id'] for tag in char_tags]
        
        # 找到玩家没有的标签
        missing_tags = []
        for tag in char_tags:
            if tag['tag_id'] not in user_tag_ids:
                missing_tags.append(tag['tag_name'])
        
        if missing_tags:
            recommendations.append({
                'character_id': char['character_id'],
                'character_name': char['name'],
                'camp_name': char['camp_name'],
                'attribute_name': char['attribute_name'],
                'fate_name': char['fate_name'],
                'missing_tags': missing_tags,
                'character_tags': [tag['tag_name'] for tag in char_tags],
                'missing_count': len(missing_tags)
            })
    
    # 按缺失标签数量降序排序
    recommendations.sort(key=lambda x: x['missing_count'], reverse=True)
    return recommendations

def get_missing_camps_recommendations(all_characters, character_tags_dict, user_camps):
    """推荐可以补充缺失阵营的角色"""
    recommendations = []
    
    for char in all_characters:
        char_id = char['character_id']
        char_tags = character_tags_dict.get(char_id, [])
        
        if char['camp_id'] not in user_camps:
            recommendations.append({
                'character_id': char['character_id'],
                'character_name': char['name'],
                'camp_name': char['camp_name'],
                'attribute_name': char['attribute_name'],
                'fate_name': char['fate_name'],
                'character_tags': [tag['tag_name'] for tag in char_tags]
            })
    
    return recommendations

def get_missing_combinations_recommendations(all_characters, character_tags_dict, user_combinations):
    """推荐可以补充缺失属性-命途组合的角色"""
    recommendations = []
    
    for char in all_characters:
        char_id = char['character_id']
        char_tags = character_tags_dict.get(char_id, [])
        combination = (char['attribute_id'], char['fate_id'])
        
        if combination not in user_combinations:
            recommendations.append({
                'character_id': char['character_id'],
                'character_name': char['name'],
                'camp_name': char['camp_name'],
                'attribute_name': char['attribute_name'],
                'fate_name': char['fate_name'],
                'character_tags': [tag['tag_name'] for tag in char_tags]
            })
    
    return recommendations

def get_high_ownership_recommendations(conn, all_characters, character_tags_dict):
    """推荐高持有率但玩家未拥有的角色"""
    recommendations = []
    
    # 获取总玩家数
    total_players = conn.execute('SELECT COUNT(*) as count FROM User WHERE user_type = "玩家"').fetchone()['count']
    
    if total_players == 0:
        return recommendations
    
    for char in all_characters:
        char_id = char['character_id']
        char_tags = character_tags_dict.get(char_id, [])
        
        # 计算该角色的持有率
        owners_count = conn.execute(
            'SELECT COUNT(*) as count FROM User_Character WHERE character_id = ?', 
            (char_id,)
        ).fetchone()['count']
        
        ownership_rate = (owners_count / total_players) * 100
        
        # 只推荐持有率超过30%的角色
        if ownership_rate >= 30:
            recommendations.append({
                'character_id': char['character_id'],
                'character_name': char['name'],
                'camp_name': char['camp_name'],
                'attribute_name': char['attribute_name'],
                'fate_name': char['fate_name'],
                'character_tags': [tag['tag_name'] for tag in char_tags],
                'ownership_rate': round(ownership_rate, 1)
            })
    
    # 按持有率降序排序
    recommendations.sort(key=lambda x: x['ownership_rate'], reverse=True)
    return recommendations

def get_ml_favor_predictions(conn, user_id, all_characters, character_tags_dict, user_characters):
    """使用机器学习预测用户对角色的好感度"""
    try:
        if len(user_characters) < 3:
            return []  # 数据太少，无法进行机器学习
        
        # 准备训练数据
        training_data = []
        for char in user_characters:
            char_tags = character_tags_dict.get(char['character_id'], [])
            char_tag_ids = [tag['tag_id'] for tag in char_tags]
            
            # 创建特征向量: [camp_id, attribute_id, fate_id, tag1_present, tag2_present, ...]
            features = [char['camp_id'], char['attribute_id'], char['fate_id']]
            
            # 获取所有可能的标签ID并创建one-hot编码
            all_tags_query = 'SELECT tag_id FROM Tag ORDER BY tag_id'
            all_tag_ids = [row['tag_id'] for row in conn.execute(all_tags_query).fetchall()]
            
            for tag_id in all_tag_ids:
                features.append(1 if tag_id in char_tag_ids else 0)
            
            training_data.append((features, char['favor']))
        
        # 如果训练数据不足，返回空列表
        if len(training_data) < 3:
            return []
        
        # 训练随机森林模型
        X = np.array([data[0] for data in training_data])
        y = np.array([data[1] for data in training_data])
        
        model = RandomForestRegressor(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        # 预测推荐角色的好感度
        recommendations = []
        all_tags_query = 'SELECT tag_id FROM Tag ORDER BY tag_id'
        all_tag_ids = [row['tag_id'] for row in conn.execute(all_tags_query).fetchall()]
        
        for char in all_characters:
            char_id = char['character_id']
            char_tags = character_tags_dict.get(char_id, [])
            char_tag_ids = [tag['tag_id'] for tag in char_tags]
            
            # 创建特征向量
            features = [char['camp_id'], char['attribute_id'], char['fate_id']]
            for tag_id in all_tag_ids:
                features.append(1 if tag_id in char_tag_ids else 0)
            
            # 预测好感度
            predicted_favor = model.predict([features])[0]
            
            # 只推荐预测好感度较高的角色(大于用户平均好感度)
            avg_favor = np.mean(y)
            if predicted_favor > avg_favor:
                recommendations.append({
                    'character_id': char['character_id'],
                    'character_name': char['name'],
                    'camp_name': char['camp_name'],
                    'attribute_name': char['attribute_name'],
                    'fate_name': char['fate_name'],
                    'character_tags': [tag['tag_name'] for tag in char_tags],
                    'predicted_favor': round(predicted_favor, 1)
                })
        
        # 按预测好感度降序排序
        recommendations.sort(key=lambda x: x['predicted_favor'], reverse=True)
        return recommendations
        
    except Exception as e:
        print(f"ML prediction error: {e}")
        return []

if __name__ == '__main__':
    app.run(debug=True) 