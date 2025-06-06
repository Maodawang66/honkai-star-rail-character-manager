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
};

// 查询角色数据
async function queryCharacters() {
    try {
        const res = await fetch('http://localhost:5000/api/characters');
        const characters = await res.json();
        
        let html = '<h3>角色数据</h3>';
        html += '<table><tr><th>ID</th><th>名称</th><th>描述</th><th>阵营</th><th>属性</th><th>命途</th><th>技能</th></tr>';
        
        for (const char of characters) {
            const campRes = await fetch(`http://localhost:5000/api/camps/${char.camp_id}`);
            const camp = await campRes.json();
            
            const attrRes = await fetch(`http://localhost:5000/api/attributes/${char.attribute_id}`);
            const attr = await attrRes.json();
            
            const fateRes = await fetch(`http://localhost:5000/api/fates/${char.fate_id}`);
            const fate = await fateRes.json();
            
            html += `
                <tr>
                    <td>${char.character_id}</td>
                    <td>${char.name}</td>
                    <td>${char.description || ''}</td>
                    <td>${camp.camp_name}</td>
                    <td>${attr.attribute_name}</td>
                    <td>${fate.fate_name}</td>
                    <td>${char.skill || ''}</td>
                </tr>
            `;
        }
        
        html += '</table>';
        document.getElementById('query-result').innerHTML = html;
    } catch (error) {
        alert('查询失败：' + error.message);
    }
}

// 查询BOSS数据
async function queryBosses() {
    try {
        const res = await fetch('http://localhost:5000/api/bosses');
        const bosses = await res.json();
        
        let html = '<h3>BOSS数据</h3>';
        html += '<table><tr><th>ID</th><th>名称</th><th>描述</th><th>阵营</th><th>弱点</th></tr>';
        
        for (const boss of bosses) {
            const campRes = await fetch(`http://localhost:5000/api/camps/${boss.camp_id}`);
            const camp = await campRes.json();
            
            const attrRes = await fetch(`http://localhost:5000/api/attributes/${boss.weakness_id}`);
            const attr = await attrRes.json();
            
            html += `
                <tr>
                    <td>${boss.boss_id}</td>
                    <td>${boss.name}</td>
                    <td>${boss.description || ''}</td>
                    <td>${camp.camp_name}</td>
                    <td>${attr.attribute_name}</td>
                </tr>
            `;
        }
        
        html += '</table>';
        document.getElementById('query-result').innerHTML = html;
    } catch (error) {
        alert('查询失败：' + error.message);
    }
}

// 查询环境数据
async function queryEnvironments() {
    try {
        const res = await fetch('http://localhost:5000/api/environments');
        const environments = await res.json();
        
        let html = '<h3>环境数据</h3>';
        html += '<table><tr><th>ID</th><th>名称</th><th>增益效果</th></tr>';
        
        for (const env of environments) {
            html += `
                <tr>
                    <td>${env.env_id}</td>
                    <td>${env.name}</td>
                    <td>${env.buff || ''}</td>
                </tr>
            `;
        }
        
        html += '</table>';
        document.getElementById('query-result').innerHTML = html;
    } catch (error) {
        alert('查询失败：' + error.message);
    }
} 