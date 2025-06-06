// 全局变量
let allCharacters = [];
let allCamps = [];
let allAttributes = [];
let allFates = [];

// 页面加载时初始化
window.onload = async function() {
    const userData = JSON.parse(localStorage.getItem('user'));
    if (!userData || !userData.user) {
        window.location.href = 'login.html';
        return;
    }
    
    const user = userData.user;
    if (user.user_type !== '策划') {
        window.location.href = 'home.html';
        return;
    }

    document.getElementById('username').textContent = user.username;
    await loadAllData();
    loadCharacterList();
};

// 加载所有基础数据
async function loadAllData() {
    try {
        // 加载阵营数据
        const campRes = await fetch('http://localhost:5000/api/camps');
        allCamps = await campRes.json();
        const campOptions = allCamps.map(c => `<option value="${c.camp_id}">${c.camp_name}</option>`).join('');
        ['a_camp', 'e_camp'].forEach(id => {
            document.getElementById(id).innerHTML = '<option value="">选择阵营</option>' + campOptions;
        });

        // 加载属性数据
        const attrRes = await fetch('http://localhost:5000/api/attributes');
        allAttributes = await attrRes.json();
        const attrOptions = allAttributes.map(a => `<option value="${a.attribute_id}">${a.attribute_name}</option>`).join('');
        ['a_attribute', 'e_attribute'].forEach(id => {
            document.getElementById(id).innerHTML = '<option value="">选择属性</option>' + attrOptions;
        });

        // 加载命途数据
        const fateRes = await fetch('http://localhost:5000/api/fates');
        allFates = await fateRes.json();
        const fateOptions = allFates.map(f => `<option value="${f.fate_id}">${f.fate_name}</option>`).join('');
        ['a_fate', 'e_fate'].forEach(id => {
            document.getElementById(id).innerHTML = '<option value="">选择命途</option>' + fateOptions;
        });

        // 加载角色数据
        const charRes = await fetch('http://localhost:5000/api/characters');
        allCharacters = await charRes.json();
    } catch (error) {
        alert('加载数据失败：' + error.message);
    }
}

// 加载角色列表
function loadCharacterList() {
    const list = document.getElementById('characterList');
    let html = '<table><tr><th>ID</th><th>名称</th><th>阵营</th><th>属性</th><th>命途</th><th>操作</th></tr>';
    
    allCharacters.forEach(char => {
        const camp = allCamps.find(c => c.camp_id === char.camp_id)?.camp_name || '';
        const attr = allAttributes.find(a => a.attribute_id === char.attribute_id)?.attribute_name || '';
        const fate = allFates.find(f => f.fate_id === char.fate_id)?.fate_name || '';
        
        html += `
            <tr>
                <td>${char.character_id}</td>
                <td>${char.name}</td>
                <td>${camp}</td>
                <td>${attr}</td>
                <td>${fate}</td>
                <td>
                    <button onclick="editCharacter(${char.character_id})">编辑</button>
                    <button onclick="deleteCharacter(${char.character_id})">删除</button>
                </td>
            </tr>
        `;
    });
    
    html += '</table>';
    list.innerHTML = html;
}

// 显示添加角色弹窗
function showAddModal() {
    document.getElementById('add-modal').style.display = 'flex';
    document.getElementById('add-form').reset();
}

// 关闭添加角色弹窗
function closeAddModal() {
    document.getElementById('add-modal').style.display = 'none';
}

// 显示修改角色弹窗
function showEditModal() {
    document.getElementById('edit-modal').style.display = 'flex';
}

// 关闭修改角色弹窗
function closeEditModal() {
    document.getElementById('edit-modal').style.display = 'none';
}

// 显示删除角色弹窗
function showDeleteModal() {
    document.getElementById('delete-modal').style.display = 'flex';
    document.getElementById('delete-form').reset();
}

// 关闭删除角色弹窗
function closeDeleteModal() {
    document.getElementById('delete-modal').style.display = 'none';
}

// 编辑角色
function editCharacter(id) {
    const char = allCharacters.find(c => c.character_id === id);
    if (!char) return;

    document.getElementById('e_name').value = char.name;
    document.getElementById('e_description').value = char.description || '';
    document.getElementById('e_camp').value = char.camp_id;
    document.getElementById('e_attribute').value = char.attribute_id;
    document.getElementById('e_fate').value = char.fate_id;
    document.getElementById('e_skill').value = char.skill || '';

    showEditModal();
}

// 删除角色
function deleteCharacter(id) {
    if (!confirm('确定要删除这个角色吗？')) return;

    fetch(`http://localhost:5000/api/characters/${id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert('删除成功');
            loadAllData();
            loadCharacterList();
        }
    })
    .catch(error => {
        alert('删除失败：' + error.message);
    });
}

// 添加角色表单提交
document.getElementById('add-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const data = {
        name: document.getElementById('a_name').value,
        description: document.getElementById('a_description').value,
        camp_id: document.getElementById('a_camp').value,
        attribute_id: document.getElementById('a_attribute').value,
        fate_id: document.getElementById('a_fate').value,
        skill: document.getElementById('a_skill').value
    };

    try {
        const res = await fetch('http://localhost:5000/api/characters', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await res.json();
        
        if (res.ok) {
            alert('添加成功');
            closeAddModal();
            loadAllData();
            loadCharacterList();
        } else {
            alert(result.error || '添加失败');
        }
    } catch (error) {
        alert('添加失败：' + error.message);
    }
});

// 修改角色表单提交
document.getElementById('edit-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const data = {
        name: document.getElementById('e_name').value,
        description: document.getElementById('e_description').value,
        camp_id: document.getElementById('e_camp').value,
        attribute_id: document.getElementById('e_attribute').value,
        fate_id: document.getElementById('e_fate').value,
        skill: document.getElementById('e_skill').value
    };

    try {
        const res = await fetch('http://localhost:5000/api/characters', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await res.json();
        
        if (res.ok) {
            alert('修改成功');
            closeEditModal();
            loadAllData();
            loadCharacterList();
        } else {
            alert(result.error || '修改失败');
        }
    } catch (error) {
        alert('修改失败：' + error.message);
    }
});

// 删除角色表单提交
document.getElementById('delete-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const name = document.getElementById('d_name').value;
    const char = allCharacters.find(c => c.name === name);
    
    if (!char) {
        alert('角色不存在');
        return;
    }

    if (!confirm('确定要删除这个角色吗？')) return;

    try {
        const res = await fetch(`http://localhost:5000/api/characters/${char.character_id}`, {
            method: 'DELETE'
        });
        const result = await res.json();
        
        if (res.ok) {
            alert('删除成功');
            closeDeleteModal();
            loadAllData();
            loadCharacterList();
        } else {
            alert(result.error || '删除失败');
        }
    } catch (error) {
        alert('删除失败：' + error.message);
    }
}); 