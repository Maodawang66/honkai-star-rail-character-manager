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
    loadFilterOptions();
};

// 加载所有基础数据
async function loadAllData() {
    try {
        // 加载阵营数据
        const campRes = await fetch('http://localhost:5000/api/camps');
        allCamps = await campRes.json();
        
        // 加载属性数据
        const attrRes = await fetch('http://localhost:5000/api/attributes');
        allAttributes = await attrRes.json();
        
        // 加载命途数据
        const fateRes = await fetch('http://localhost:5000/api/fates');
        allFates = await fateRes.json();
        
        // 加载角色数据
        const charRes = await fetch('http://localhost:5000/api/characters');
        allCharacters = await charRes.json();
        
        // 初始显示所有角色
        displayCharacters(allCharacters);
    } catch (error) {
        alert('加载数据失败：' + error.message);
    }
}

// 加载筛选选项
function loadFilterOptions() {
    // 加载阵营选项
    const campOptions = allCamps.map(c => `<option value="${c.camp_id}">${c.camp_name}</option>`).join('');
    document.getElementById('campFilter').innerHTML = '<option value="">所有阵营</option>' + campOptions;
    
    // 加载属性选项
    const attrOptions = allAttributes.map(a => `<option value="${a.attribute_id}">${a.attribute_name}</option>`).join('');
    document.getElementById('attributeFilter').innerHTML = '<option value="">所有属性</option>' + attrOptions;
    
    // 加载命途选项
    const fateOptions = allFates.map(f => `<option value="${f.fate_id}">${f.fate_name}</option>`).join('');
    document.getElementById('fateFilter').innerHTML = '<option value="">所有命途</option>' + fateOptions;
}

// 搜索角色
function searchCharacters() {
    const keyword = document.getElementById('searchInput').value.toLowerCase();
    const campId = document.getElementById('campFilter').value;
    const attrId = document.getElementById('attributeFilter').value;
    const fateId = document.getElementById('fateFilter').value;
    
    const filtered = allCharacters.filter(char => {
        const matchKeyword = !keyword || 
            char.name.toLowerCase().includes(keyword) ||
            char.description?.toLowerCase().includes(keyword) ||
            char.skill?.toLowerCase().includes(keyword);
            
        const matchCamp = !campId || char.camp_id === parseInt(campId);
        const matchAttr = !attrId || char.attribute_id === parseInt(attrId);
        const matchFate = !fateId || char.fate_id === parseInt(fateId);
        
        return matchKeyword && matchCamp && matchAttr && matchFate;
    });
    
    displayCharacters(filtered);
}

// 显示角色列表
function displayCharacters(characters) {
    const list = document.getElementById('character-list');
    let html = '<table><tr><th>ID</th><th>名称</th><th>描述</th><th>阵营</th><th>属性</th><th>命途</th><th>技能</th></tr>';
    
    characters.forEach(char => {
        const camp = allCamps.find(c => c.camp_id === char.camp_id)?.camp_name || '';
        const attr = allAttributes.find(a => a.attribute_id === char.attribute_id)?.attribute_name || '';
        const fate = allFates.find(f => f.fate_id === char.fate_id)?.fate_name || '';
        
        html += `
            <tr>
                <td>${char.character_id}</td>
                <td>${char.name}</td>
                <td>${char.description || ''}</td>
                <td>${camp}</td>
                <td>${attr}</td>
                <td>${fate}</td>
                <td>${char.skill || ''}</td>
            </tr>
        `;
    });
    
    html += '</table>';
    list.innerHTML = html;
}

// 标签切换
const tabs = ['character', 'boss', 'env', 'stat'];
tabs.forEach(tab => {
    document.getElementById('tab-' + tab).onclick = function() {
        tabs.forEach(t => {
            document.getElementById('tab-' + t).classList.remove('active');
            document.getElementById('section-' + t).style.display = 'none';
        });
        this.classList.add('active');
        document.getElementById('section-' + tab).style.display = '';
    };
});

// 角色库
let myCharacters = [];
async function loadMyCharacters() {
    const res = await fetch(`http://localhost:5000/api/user_characters/${user.user_id}`);
    myCharacters = await res.json();
}
function renderCharacterTable(data) {
    let html = '<table><tr><th>角色ID</th><th>名称</th><th>星魂</th><th>等级</th><th>战力</th><th>好感度</th></tr>';
    data.forEach(row => {
        html += `<tr><td>${row.character_id}</td><td>${row.name||''}</td><td>${row.star_soul||''}</td><td>${row.level||''}</td><td>${row.power||''}</td><td>${row.favor||''}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('character-result').innerHTML = html;
}
function renderCharacterSimpleTable(data) {
    let html = '<table><tr><th>角色ID</th><th>名称</th></tr>';
    data.forEach(row => {
        html += `<tr><td>${row.character_id}</td><td>${row.name||''}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('character-result').innerHTML = html;
}
// 查询已获得角色
async function showMyCharacters() {
    await loadAllData();
    await loadMyCharacters();
    // myCharacters 只包含已获得
    renderCharacterTable(myCharacters);
}
// 查询未获得角色
async function showMissingCharacters() {
    await loadAllData();
    await loadMyCharacters();
    const myIds = myCharacters.map(c => c.character_id);
    const missing = allCharacters.filter(c => !myIds.includes(c.character_id));
    renderCharacterSimpleTable(missing);
}
// 关键词查询
async function searchCharacter() {
    await loadAllData();
    const kw = document.getElementById('search-character').value.trim();
    let data = allCharacters;
    if (kw) data = data.filter(c => c.name.includes(kw));
    renderCharacterSimpleTable(data);
}
document.getElementById('btn-my-characters').onclick = showMyCharacters;
document.getElementById('btn-missing-characters').onclick = showMissingCharacters;
document.getElementById('btn-search-character').onclick = searchCharacter;

// BOSS库
async function searchBoss() {
    const kw = document.getElementById('search-boss').value.trim();
    const res = await fetch('http://localhost:5000/api/bosses');
    let data = await res.json();
    if (kw) data = data.filter(b => b.name.includes(kw));
    let html = '<table><tr><th>BOSS ID</th><th>名称</th><th>简介</th><th>阵营ID</th><th>弱点属性ID</th></tr>';
    data.forEach(b => {
        html += `<tr><td>${b.boss_id}</td><td>${b.name}</td><td>${b.description||''}</td><td>${b.camp_id||''}</td><td>${b.weakness_id||''}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('boss-result').innerHTML = html;
}
document.getElementById('btn-search-boss').onclick = searchBoss;

// 环境库
async function searchEnv() {
    const kw = document.getElementById('search-env').value.trim();
    const res = await fetch('http://localhost:5000/api/environments');
    let data = await res.json();
    if (kw) data = data.filter(e => e.name.includes(kw));
    let html = '<table><tr><th>环境ID</th><th>名称</th><th>BUFF</th></tr>';
    data.forEach(e => {
        html += `<tr><td>${e.env_id}</td><td>${e.name}</td><td>${e.buff||''}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('env-result').innerHTML = html;
}
document.getElementById('btn-search-env').onclick = searchEnv;

// 统计信息
async function fetchStat(url, render) {
    const res = await fetch(url);
    const data = await res.json();
    render(data);
}
function renderPowerRankTable(data) {
    let html = '<table><tr><th>排名</th><th>角色名称</th><th>平均战力</th></tr>';
    data.forEach((row, idx) => {
        html += `<tr><td>${idx+1}</td><td>${row.name}</td><td>${row.avg_power}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('stat-result').innerHTML = html;
}
function renderHoldRateTable(data) {
    let html = '<table><tr><th>角色名称</th><th>持有人数</th><th>持有率</th></tr>';
    data.forEach(row => {
        html += `<tr><td>${row.name}</td><td>${row.user_count}</td><td>${(row.hold_rate*100).toFixed(2)}%</td></tr>`;
    });
    html += '</table>';
    document.getElementById('stat-result').innerHTML = html;
}
// 全服战力排行
function statPowerRankAll() {
    const name = document.getElementById('stat-character-name').value.trim();
    let url = 'http://localhost:5000/api/stat/character_power_rank';
    if (name) url += `?name=${encodeURIComponent(name)}`;
    fetchStat(url, renderPowerRankTable);
}
// 玩家战力排行
function statPowerRankUser() {
    const name = document.getElementById('stat-character-name').value.trim();
    let url = `http://localhost:5000/api/stat/character_power_rank?user_id=${user.user_id}`;
    if (name) url += `&name=${encodeURIComponent(name)}`;
    fetchStat(url, renderPowerRankTable);
}
// 全服持有率
function statHoldRateAll() {
    const name = document.getElementById('stat-character-name').value.trim();
    let url = 'http://localhost:5000/api/stat/character_hold_rate';
    if (name) url += `?name=${encodeURIComponent(name)}`;
    fetchStat(url, renderHoldRateTable);
}
// 玩家持有率
function statHoldRateUser() {
    const name = document.getElementById('stat-character-name').value.trim();
    let url = `http://localhost:5000/api/stat/character_hold_rate?user_id=${user.user_id}`;
    if (name) url += `&name=${encodeURIComponent(name)}`;
    fetchStat(url, renderHoldRateTable);
}
document.getElementById('btn-power-rank-all').onclick = statPowerRankAll;
document.getElementById('btn-power-rank-user').onclick = statPowerRankUser;
document.getElementById('btn-hold-rate-all').onclick = statHoldRateAll;
document.getElementById('btn-hold-rate-user').onclick = statHoldRateUser;

// 默认加载我的角色
showMyCharacters(); 