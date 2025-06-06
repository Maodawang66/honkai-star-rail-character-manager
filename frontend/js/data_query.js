// 数据查询页面脚本

// 角色、BOSS、环境、命途、阵营、属性、标签数据
let allCharacters = [], allCharacterTags = [], allTags = [];
let allBosses = [], allBossTags = [];
let allEnvs = [], allEnvTags = [];
let allFates = [], allCamps = [], allAttributes = [];

// 获取所有标签
function loadTags() {
    return fetch('http://localhost:5000/api/tags').then(res => res.json()).then(data => { allTags = data; });
}
// 获取所有角色-标签
function loadCharacterTags() {
    return fetch('http://localhost:5000/api/character_tags').then(res => res.json()).then(data => { allCharacterTags = data; });
}
// 获取所有BOSS-标签
function loadBossTags() {
    return fetch('http://localhost:5000/api/boss_tags').then(res => res.json()).then(data => { allBossTags = data; });
}
// 获取所有环境-标签
function loadEnvTags() {
    return fetch('http://localhost:5000/api/environment_tags').then(res => res.json()).then(data => { allEnvTags = data; });
}

function getTagNamesByIds(tagIds) {
    return tagIds.map(id => {
        const tag = allTags.find(t => t.tag_id == id);
        return tag ? tag.name : id;
    }).join('，');
}

// 渲染角色列表，带标签
function renderCharacterList(data) {
    let html = '<table><tr><th>ID</th><th>名称</th><th>简介</th><th>阵营ID</th><th>属性ID</th><th>命途ID</th><th>技能</th><th>标签</th></tr>';
    data.forEach(c => {
        const tagIds = allCharacterTags.filter(ct => ct.character_id == c.character_id).map(ct => ct.tag_id);
        const tagNames = getTagNamesByIds(tagIds);
        html += `<tr><td>${c.character_id}</td><td>${c.name}</td><td>${c.description || ''}</td><td>${c.camp_id || ''}</td><td>${c.attribute_id || ''}</td><td>${c.fate_id || ''}</td><td>${c.skill || ''}</td><td>${tagNames}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('character-list').innerHTML = html;
}
// 渲染BOSS列表，带标签
function renderBossList(data) {
    let html = '<table><tr><th>ID</th><th>名称</th><th>简介</th><th>阵营ID</th><th>弱点属性ID</th><th>标签</th></tr>';
    data.forEach(b => {
        const tagIds = allBossTags.filter(bt => bt.boss_id == b.boss_id).map(bt => bt.tag_id);
        const tagNames = getTagNamesByIds(tagIds);
        html += `<tr><td>${b.boss_id}</td><td>${b.name}</td><td>${b.description || ''}</td><td>${b.camp_id || ''}</td><td>${b.weakness_id || ''}</td><td>${tagNames}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('boss-list').innerHTML = html;
}
// 渲染环境列表，带标签
function renderEnvList(data) {
    let html = '<table><tr><th>ID</th><th>名称</th><th>Buff</th><th>标签</th></tr>';
    data.forEach(e => {
        const tagIds = allEnvTags.filter(et => et.env_id == e.env_id).map(et => et.tag_id);
        const tagNames = getTagNamesByIds(tagIds);
        html += `<tr><td>${e.env_id}</td><td>${e.name}</td><td>${e.buff || ''}</td><td>${tagNames}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('env-list').innerHTML = html;
}
// 渲染命途
function renderFateList(data) {
    let html = '<table><tr><th>ID</th><th>名称</th></tr>';
    data.forEach(f => {
        html += `<tr><td>${f.fate_id}</td><td>${f.fate_name}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('fate-list').innerHTML = html;
}
// 渲染阵营
function renderCampList(data) {
    let html = '<table><tr><th>ID</th><th>名称</th></tr>';
    data.forEach(c => {
        html += `<tr><td>${c.camp_id}</td><td>${c.camp_name}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('camp-list').innerHTML = html;
}
// 渲染属性
function renderAttributeList(data) {
    let html = '<table><tr><th>ID</th><th>名称</th></tr>';
    data.forEach(a => {
        html += `<tr><td>${a.attribute_id}</td><td>${a.attribute_name}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('attribute-list').innerHTML = html;
}
// 渲染标签
function renderTagList(data) {
    let html = '<table><tr><th>ID</th><th>名称</th></tr>';
    data.forEach(t => {
        html += `<tr><td>${t.tag_id}</td><td>${t.name}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('tag-list').innerHTML = html;
}

// 搜索功能
function addSearch(inputId, data, renderFunc, filterFunc) {
    document.getElementById(inputId).addEventListener('input', function() {
        const val = this.value.trim();
        if (!val) {
            renderFunc(data);
        } else {
            renderFunc(data.filter(item => filterFunc(item, val)));
        }
    });
}

// 统计弹窗展示
function showStatDialog(title, html) {
    const dialog = document.createElement('div');
    dialog.style.position = 'fixed';
    dialog.style.left = '0';
    dialog.style.top = '0';
    dialog.style.width = '100vw';
    dialog.style.height = '100vh';
    dialog.style.background = 'rgba(0,0,0,0.3)';
    dialog.style.zIndex = '9999';
    dialog.innerHTML = `<div style="background:#fff;padding:32px 24px;max-width:600px;margin:80px auto;border-radius:10px;box-shadow:0 2px 16px #0002;position:relative;">
        <h2 style='margin-top:0;'>${title}</h2>
        <div>${html}</div>
        <button id='close-stat-dialog' style='margin-top:24px;'>关闭</button>
    </div>`;
    document.body.appendChild(dialog);
    document.getElementById('close-stat-dialog').onclick = () => dialog.remove();
}

// 查询全服角色战力排行（可指定角色名或全部）
async function fetchPowerRank(single) {
    let url = 'http://localhost:5000/api/stat/character_power_rank';
    let title = '全服角色战力排行';
    if (single) {
        const name = document.getElementById('input-power-rank').value.trim();
        if (!name) { alert('请输入角色名称'); return; }
        url += `?name=${encodeURIComponent(name)}`;
        title += ` - ${name}`;
    }
    const res = await fetch(url);
    const data = await res.json();
    let html = '<table><tr><th>排名</th><th>角色名称</th><th>平均战力</th></tr>';
    data.forEach((row, idx) => {
        html += `<tr><td>${idx+1}</td><td>${row.name}</td><td>${row.avg_power}</td></tr>`;
    });
    html += '</table>';
    showStatDialog(title, html);
}
// 查询角色持有率（可指定角色名或全部）
async function fetchHoldRate(single) {
    let url = 'http://localhost:5000/api/stat/character_hold_rate';
    let title = '角色持有率统计';
    if (single) {
        const name = document.getElementById('input-hold-rate').value.trim();
        if (!name) { alert('请输入角色名称'); return; }
        url += `?name=${encodeURIComponent(name)}`;
        title += ` - ${name}`;
    }
    const res = await fetch(url);
    const data = await res.json();
    let html = '<table><tr><th>角色名称</th><th>持有人数</th><th>持有率</th></tr>';
    data.forEach(row => {
        html += `<tr><td>${row.name}</td><td>${row.user_count}</td><td>${(row.hold_rate*100).toFixed(2)}%</td></tr>`;
    });
    html += '</table>';
    showStatDialog(title, html);
}

// 初始化加载所有数据
async function init() {
    await loadTags();
    await Promise.all([
        fetch('http://localhost:5000/api/characters').then(res => res.json()).then(data => { allCharacters = data; }),
        fetch('http://localhost:5000/api/bosses').then(res => res.json()).then(data => { allBosses = data; }),
        fetch('http://localhost:5000/api/environments').then(res => res.json()).then(data => { allEnvs = data; }),
        fetch('http://localhost:5000/api/fates').then(res => res.json()).then(data => { allFates = data; }),
        fetch('http://localhost:5000/api/camps').then(res => res.json()).then(data => { allCamps = data; }),
        fetch('http://localhost:5000/api/attributes').then(res => res.json()).then(data => { allAttributes = data; })
    ]);
    await Promise.all([
        loadCharacterTags(),
        loadBossTags(),
        loadEnvTags()
    ]);
    renderCharacterList(allCharacters);
    renderBossList(allBosses);
    renderEnvList(allEnvs);
    renderFateList(allFates);
    renderCampList(allCamps);
    renderAttributeList(allAttributes);
    renderTagList(allTags);

    addSearch('search-character', allCharacters, renderCharacterList, (item, val) => item.name.includes(val) || (item.description && item.description.includes(val)));
    addSearch('search-boss', allBosses, renderBossList, (item, val) => item.name.includes(val) || (item.description && item.description.includes(val)));
    addSearch('search-env', allEnvs, renderEnvList, (item, val) => item.name.includes(val) || (item.buff && item.buff.includes(val)));
    addSearch('search-fate', allFates, renderFateList, (item, val) => item.fate_name.includes(val));
    addSearch('search-camp', allCamps, renderCampList, (item, val) => item.camp_name.includes(val));
    addSearch('search-attribute', allAttributes, renderAttributeList, (item, val) => item.attribute_name.includes(val));
    addSearch('search-tag', allTags, renderTagList, (item, val) => item.name.includes(val));
}

window.onload = function() {
    init();
    document.getElementById('btn-all-character').onclick = function() {
        document.getElementById('search-character').value = '';
        renderCharacterList(allCharacters);
    };
    document.getElementById('btn-all-boss').onclick = function() {
        document.getElementById('search-boss').value = '';
        renderBossList(allBosses);
    };
    document.getElementById('btn-all-env').onclick = function() {
        document.getElementById('search-env').value = '';
        renderEnvList(allEnvs);
    };
    document.getElementById('btn-all-fate').onclick = function() {
        document.getElementById('search-fate').value = '';
        renderFateList(allFates);
    };
    document.getElementById('btn-all-camp').onclick = function() {
        document.getElementById('search-camp').value = '';
        renderCampList(allCamps);
    };
    document.getElementById('btn-all-attribute').onclick = function() {
        document.getElementById('search-attribute').value = '';
        renderAttributeList(allAttributes);
    };
    document.getElementById('btn-all-tag').onclick = function() {
        document.getElementById('search-tag').value = '';
        renderTagList(allTags);
    };
    document.getElementById('btn-power-rank').onclick = function() { fetchPowerRank(true); };
    document.getElementById('btn-all-power-rank').onclick = function() { fetchPowerRank(false); };
    document.getElementById('btn-hold-rate').onclick = function() { fetchHoldRate(true); };
    document.getElementById('btn-all-hold-rate').onclick = function() { fetchHoldRate(false); };
    // 查询单个对象按钮
    document.getElementById('btn-single-character').onclick = function() {
        const val = document.getElementById('search-character').value.trim();
        if (!val) { alert('请输入角色名称'); return; }
        renderCharacterList(allCharacters.filter(item => item.name === val));
    };
    document.getElementById('btn-single-boss').onclick = function() {
        const val = document.getElementById('search-boss').value.trim();
        if (!val) { alert('请输入BOSS名称'); return; }
        renderBossList(allBosses.filter(item => item.name === val));
    };
    document.getElementById('btn-single-env').onclick = function() {
        const val = document.getElementById('search-env').value.trim();
        if (!val) { alert('请输入环境名称'); return; }
        renderEnvList(allEnvs.filter(item => item.name === val));
    };
    document.getElementById('btn-single-fate').onclick = function() {
        const val = document.getElementById('search-fate').value.trim();
        if (!val) { alert('请输入命途名称'); return; }
        renderFateList(allFates.filter(item => item.fate_name === val));
    };
    document.getElementById('btn-single-camp').onclick = function() {
        const val = document.getElementById('search-camp').value.trim();
        if (!val) { alert('请输入阵营名称'); return; }
        renderCampList(allCamps.filter(item => item.camp_name === val));
    };
    document.getElementById('btn-single-attribute').onclick = function() {
        const val = document.getElementById('search-attribute').value.trim();
        if (!val) { alert('请输入属性名称'); return; }
        renderAttributeList(allAttributes.filter(item => item.attribute_name === val));
    };
    document.getElementById('btn-single-tag').onclick = function() {
        const val = document.getElementById('search-tag').value.trim();
        if (!val) { alert('请输入标签名称'); return; }
        renderTagList(allTags.filter(item => item.name === val));
    };
}; 