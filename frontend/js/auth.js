// 检查是否已登录
function checkAuth() {
    const user = localStorage.getItem('user');
    if (!user && !window.location.href.includes('login.html') && !window.location.href.includes('register.html')) {
        window.location.href = 'login.html';
    }
}

// 监听用户类型选择
if (document.getElementById('userType')) {
    document.getElementById('userType').addEventListener('change', function() {
        const keyGroup = document.getElementById('keyGroup');
        if (this.value === '策划') {
            keyGroup.style.display = 'block';
            document.getElementById('key').required = true;
        } else {
            keyGroup.style.display = 'none';
            document.getElementById('key').required = false;
        }
    });
}

// 登录处理
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                localStorage.setItem('user', JSON.stringify(data));
                // 登录后根据用户类型跳转
                const userType = data.user.user_type;
                if (userType === '策划') {
                    window.location.href = 'planner_home.html';
                } else {
                    window.location.href = 'home.html';
                }
            }
        })
        .catch(error => {
            alert('登录失败，请检查网络连接或服务器状态');
        });
    });
}

// 注册处理
if (document.getElementById('registerForm')) {
    document.getElementById('registerForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const userType = document.getElementById('userType').value;
        const key = document.getElementById('key').value;

        if (password !== confirmPassword) {
            alert('两次输入的密码不一致');
            return;
        }

        // 验证策划密钥
        if (userType === '策划' && key !== '52648') {
            alert('策划密钥错误');
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password, user_type: userType })
            });

            const data = await response.json();

            if (response.ok) {
                alert('注册成功，请登录');
                window.location.href = 'login.html';
            } else {
                alert(data.error || '注册失败');
            }
        } catch (error) {
            alert('注册失败，请稍后重试');
        }
    });
}

// 退出登录
function logout() {
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

// 页面加载时检查登录状态
checkAuth();

// 全局变量存储角色列表
let allCharacters = [];

// 加载所有角色并填充下拉框
async function loadAllCharactersToSelect() {
    const res = await fetch('http://localhost:5000/api/characters');
    allCharacters = await res.json();
    const mSelect = document.getElementById('m_character_name');
    const dSelect = document.getElementById('d_character_name');
    mSelect.innerHTML = '<option value="">请选择角色名称</option>';
    dSelect.innerHTML = '<option value="">请选择角色名称</option>';
    allCharacters.forEach(c => {
        mSelect.innerHTML += `<option value="${c.character_id}">${c.name}</option>`;
        dSelect.innerHTML += `<option value="${c.character_id}">${c.name}</option>`;
    });
}

// 自动补全函数
function setupAutocomplete(inputId, listId, isDelete) {
    const input = document.getElementById(inputId);
    const list = document.getElementById(listId);
    input.addEventListener('input', function() {
        const val = this.value.trim();
        list.innerHTML = '';
        if (!val) return;
        const matches = allCharacters.filter(c => c.name.includes(val));
        matches.slice(0, 10).forEach(c => {
            const div = document.createElement('div');
            div.textContent = c.name;
            div.style.cssText = 'background:#fff;border:1px solid #ccc;padding:4px 8px;cursor:pointer;';
            div.onclick = function() {
                input.value = c.name;
                list.innerHTML = '';
            };
            list.appendChild(div);
        });
    });
    // 失焦时隐藏建议
    input.addEventListener('blur', function() { setTimeout(()=>{list.innerHTML='';}, 200); });
}

// 玩家角色维护/查询弹窗逻辑
if (window.location.pathname.includes('home.html')) {
    window.onload = function() {
        const userData = JSON.parse(localStorage.getItem('user'));
        if (!userData || !userData.user) return;
        const user = userData.user;
        if (user.user_type === '玩家') {
            document.getElementById('player-actions').style.display = 'block';
            loadAllCharactersToSelect(); // 只加载allCharacters
            setupAutocomplete('m_character_name', 'm_autocomplete', false);
            setupAutocomplete('d_character_name', 'd_autocomplete', true);
            // 弹窗显示/关闭
            document.getElementById('btn-maintain').onclick = function() {
                document.getElementById('maintain-modal').style.display = 'flex';
                loadAllCharactersToSelect();
            };
            document.getElementById('btn-query').onclick = function() {
                document.getElementById('query-modal').style.display = 'flex';
                loadUserCharacters();
            };
            document.getElementById('close-maintain').onclick = function() {
                document.getElementById('maintain-modal').style.display = 'none';
            };
            document.getElementById('close-query').onclick = function() {
                document.getElementById('query-modal').style.display = 'none';
            };

            // 角色维护：添加/修改
            document.getElementById('maintain-form').onsubmit = async function(e) {
                e.preventDefault();
                const name = document.getElementById('m_character_name').value.trim();
                const found = allCharacters.find(c => c.name === name);
                if (!found) { alert('角色名称不存在，请选择自动补全建议'); return; }
                const character_id = found.character_id;
                const star_soul = document.getElementById('m_star_soul').value || 0;
                const level = document.getElementById('m_level').value || 1;
                const favor = document.getElementById('m_favor').value || 0;
                const data = { user_id: user.user_id, character_id, star_soul, level, favor };
                // 先尝试POST（添加），如已存在则PUT（修改）
                let res = await fetch('http://localhost:5000/api/user_characters', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                let result = await res.json();
                if (res.ok) {
                    alert(result.message || '添加成功');
                } else if (result.error && result.error.includes('已存在')) {
                    // 已存在则修改
                    res = await fetch('http://localhost:5000/api/user_characters', {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    result = await res.json();
                    if (res.ok) alert(result.message || '修改成功');
                    else alert(result.error || '修改失败');
                } else {
                    alert(result.error || '操作失败');
                }
                this.reset();
                loadAllCharactersToSelect();
            };
            // 角色维护：删除
            document.getElementById('delete-form').onsubmit = async function(e) {
                e.preventDefault();
                const name = document.getElementById('d_character_name').value.trim();
                const found = allCharacters.find(c => c.name === name);
                if (!found) { alert('角色名称不存在，请选择自动补全建议'); return; }
                const character_id = found.character_id;
                const res = await fetch(`http://localhost:5000/api/user_characters/${user.user_id}/${character_id}`, {
                    method: 'DELETE'
                });
                const result = await res.json();
                if (res.ok) alert(result.message || '删除成功');
                else alert(result.error || '删除失败');
                this.reset();
                loadAllCharactersToSelect();
            };
            // 角色查询：加载并渲染
            async function loadUserCharacters(keyword) {
                let url = `http://localhost:5000/api/user_characters/${user.user_id}`;
                const res = await fetch(url);
                let data = await res.json();
                if (keyword) {
                    data = data.filter(item =>
                        (item.character_id+'' === keyword) ||
                        (item.name && item.name.includes(keyword)) ||
                        (item.level+'' === keyword) ||
                        (item.power+'' === keyword)
                    );
                }
                let html = '<table style="width:100%;border-collapse:collapse;"><tr><th>角色ID</th><th>角色名</th><th>星魂</th><th>等级</th><th>战力</th><th>好感度</th></tr>';
                data.forEach(row => {
                    html += `<tr><td>${row.character_id}</td><td>${row.name||''}</td><td>${row.star_soul}</td><td>${row.level}</td><td>${row.power}</td><td>${row.favor}</td></tr>`;
                });
                html += '</table>';
                document.getElementById('query-result').innerHTML = html;
            }
            document.getElementById('btn-search').onclick = function() {
                const kw = document.getElementById('q_keyword').value.trim();
                loadUserCharacters(kw);
            };
        }
    };
} 