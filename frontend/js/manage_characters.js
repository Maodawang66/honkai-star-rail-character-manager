// 检查是否为策划
const userData = JSON.parse(localStorage.getItem('user'));
const user = userData && userData.user;
if (!user || user.user_type !== '策划') {
    alert('无权访问');
    window.location.href = 'home.html';
}

// 角色列表和搜索
let allCharacters = [];
function loadCharacters() {
    fetch('http://localhost:5000/api/characters')
        .then(res => res.json())
        .then(data => {
            allCharacters = data;
            renderCharacterList(data);
        });
}
function renderCharacterList(data) {
    let html = '<table><tr><th>ID</th><th>名称</th><th>简介</th><th>阵营ID</th><th>属性ID</th><th>命途ID</th><th>技能</th></tr>';
    data.forEach(c => {
        html += `<tr>
            <td>${c.character_id}</td>
            <td>${c.name}</td>
            <td>${c.description || ''}</td>
            <td>${c.camp_id || ''}</td>
            <td>${c.attribute_id || ''}</td>
            <td>${c.fate_id || ''}</td>
            <td>${c.skill || ''}</td>
        </tr>`;
    });
    html += '</table>';
    document.getElementById('character-list').innerHTML = html;
}
document.getElementById('search-character').addEventListener('input', function() {
    const val = this.value.trim();
    if (!val) return renderCharacterList(allCharacters);
    const filtered = allCharacters.filter(c =>
        (c.name && c.name.includes(val)) ||
        (c.description && c.description.includes(val)) ||
        (c.skill && c.skill.includes(val))
    );
    renderCharacterList(filtered);
});
loadCharacters();

// 新增角色（不传ID）
document.getElementById('addCharacterForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const data = {
        name: document.getElementById('name').value,
        description: document.getElementById('description').value,
        camp_id: document.getElementById('camp_id').value || null,
        attribute_id: document.getElementById('attribute_id').value || null,
        fate_id: document.getElementById('fate_id').value || null,
        skill: document.getElementById('skill').value
    };
    fetch('http://localhost:5000/api/characters', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadCharacters();
        document.getElementById('addCharacterForm').reset();
    });
});

// 删除角色
document.getElementById('deleteCharacterForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const character_id = document.getElementById('delete_character_id').value;
    fetch(`http://localhost:5000/api/characters/${character_id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadCharacters();
        document.getElementById('deleteCharacterForm').reset();
    });
});

// 命途列表和搜索
let allFates = [];
function loadFates() {
    fetch('http://localhost:5000/api/fates')
        .then(res => res.json())
        .then(data => {
            allFates = data;
            renderFateList(data);
        });
}
function renderFateList(data) {
    let html = '<table><tr><th>ID</th><th>名称</th></tr>';
    data.forEach(f => {
        html += `<tr><td>${f.fate_id}</td><td>${f.fate_name}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('fate-list').innerHTML = html;
}
document.getElementById('search-fate').addEventListener('input', function() {
    const val = this.value.trim();
    if (!val) return renderFateList(allFates);
    const filtered = allFates.filter(f => f.fate_name && f.fate_name.includes(val));
    renderFateList(filtered);
});
loadFates();

// 添加命途（不传ID）
document.getElementById('addFateForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const data = {
        fate_name: document.getElementById('fate_name').value
    };
    fetch('http://localhost:5000/api/fates', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadFates();
        document.getElementById('addFateForm').reset();
    });
});

// 删除命途
document.getElementById('deleteFateForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const fate_id = document.getElementById('delete_fate_id').value;
    fetch(`http://localhost:5000/api/fates/${fate_id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadFates();
        document.getElementById('deleteFateForm').reset();
    });
});

// 阵营列表和搜索
let allCamps = [];
function loadCamps() {
    fetch('http://localhost:5000/api/camps')
        .then(res => res.json())
        .then(data => {
            allCamps = data;
            renderCampList(data);
        });
}
function renderCampList(data) {
    let html = '<table><tr><th>ID</th><th>名称</th></tr>';
    data.forEach(c => {
        html += `<tr><td>${c.camp_id}</td><td>${c.camp_name}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('camp-list').innerHTML = html;
}
document.getElementById('search-camp').addEventListener('input', function() {
    const val = this.value.trim();
    if (!val) return renderCampList(allCamps);
    const filtered = allCamps.filter(c => c.camp_name && c.camp_name.includes(val));
    renderCampList(filtered);
});
loadCamps();

// 添加阵营（不传ID）
document.getElementById('addCampForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const data = {
        camp_name: document.getElementById('camp_name').value
    };
    fetch('http://localhost:5000/api/camps', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadCamps();
        document.getElementById('addCampForm').reset();
    });
});

// 删除阵营
document.getElementById('deleteCampForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const camp_id = document.getElementById('delete_camp_id').value;
    fetch(`http://localhost:5000/api/camps/${camp_id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadCamps();
        document.getElementById('deleteCampForm').reset();
    });
});

// 属性列表和搜索
let allAttributes = [];
function loadAttributes() {
    fetch('http://localhost:5000/api/attributes')
        .then(res => res.json())
        .then(data => {
            allAttributes = data;
            renderAttributeList(data);
        });
}
function renderAttributeList(data) {
    let html = '<table><tr><th>ID</th><th>名称</th></tr>';
    data.forEach(a => {
        html += `<tr><td>${a.attribute_id}</td><td>${a.attribute_name}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('attribute-list').innerHTML = html;
}
document.getElementById('search-attribute').addEventListener('input', function() {
    const val = this.value.trim();
    if (!val) return renderAttributeList(allAttributes);
    const filtered = allAttributes.filter(a => a.attribute_name && a.attribute_name.includes(val));
    renderAttributeList(filtered);
});
loadAttributes();

// 添加属性（不传ID）
document.getElementById('addAttributeForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const data = {
        attribute_name: document.getElementById('attribute_name').value
    };
    fetch('http://localhost:5000/api/attributes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadAttributes();
        document.getElementById('addAttributeForm').reset();
    });
});

// 删除属性
document.getElementById('deleteAttributeForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const attribute_id = document.getElementById('delete_attribute_id').value;
    fetch(`http://localhost:5000/api/attributes/${attribute_id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadAttributes();
        document.getElementById('deleteAttributeForm').reset();
    });
});

// 环境列表和搜索
let allEnvs = [];
function loadEnvs() {
    fetch('http://localhost:5000/api/environments')
        .then(res => res.json())
        .then(data => {
            allEnvs = data;
            renderEnvList(data);
        });
}
function renderEnvList(data) {
    let html = '<table><tr><th>ID</th><th>名称</th><th>Buff</th></tr>';
    data.forEach(e => {
        html += `<tr><td>${e.env_id}</td><td>${e.name}</td><td>${e.buff || ''}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('env-list').innerHTML = html;
}
document.getElementById('search-env').addEventListener('input', function() {
    const val = this.value.trim();
    if (!val) return renderEnvList(allEnvs);
    const filtered = allEnvs.filter(e => (e.name && e.name.includes(val)) || (e.buff && e.buff.includes(val)));
    renderEnvList(filtered);
});
loadEnvs();

// 添加环境（不传ID）
document.getElementById('addEnvironmentForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const data = {
        name: document.getElementById('env_name').value,
        buff: document.getElementById('buff').value
    };
    fetch('http://localhost:5000/api/environments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadEnvs();
        document.getElementById('addEnvironmentForm').reset();
    });
});

// 删除环境
document.getElementById('deleteEnvironmentForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const env_id = document.getElementById('delete_env_id').value;
    fetch(`http://localhost:5000/api/environments/${env_id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadEnvs();
        document.getElementById('deleteEnvironmentForm').reset();
    });
});

// BOSS列表和搜索
let allBosses = [];
function loadBosses() {
    fetch('http://localhost:5000/api/bosses')
        .then(res => res.json())
        .then(data => {
            allBosses = data;
            renderBossList(data);
        });
}
function renderBossList(data) {
    let html = '<table><tr><th>ID</th><th>名称</th><th>简介</th><th>阵营ID</th><th>弱点属性ID</th></tr>';
    data.forEach(b => {
        html += `<tr><td>${b.boss_id}</td><td>${b.name}</td><td>${b.description || ''}</td><td>${b.camp_id || ''}</td><td>${b.weakness_id || ''}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('boss-list').innerHTML = html;
}
document.getElementById('search-boss').addEventListener('input', function() {
    const val = this.value.trim();
    if (!val) return renderBossList(allBosses);
    const filtered = allBosses.filter(b => (b.name && b.name.includes(val)) || (b.description && b.description.includes(val)));
    renderBossList(filtered);
});
loadBosses();

// 添加BOSS（不传ID）
document.getElementById('addBossForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const data = {
        name: document.getElementById('boss_name').value,
        description: document.getElementById('boss_description').value,
        camp_id: document.getElementById('boss_camp_id').value || null,
        weakness_id: document.getElementById('boss_weakness_id').value || null
    };
    fetch('http://localhost:5000/api/bosses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadBosses();
        document.getElementById('addBossForm').reset();
    });
});

// 删除BOSS
document.getElementById('deleteBossForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const boss_id = document.getElementById('delete_boss_id').value;
    fetch(`http://localhost:5000/api/bosses/${boss_id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadBosses();
        document.getElementById('deleteBossForm').reset();
    });
});

// 标签列表和搜索
let allTags = [];
function loadTags() {
    fetch('http://localhost:5000/api/tags')
        .then(res => res.json())
        .then(data => {
            allTags = data;
            renderTagList(data);
        });
}
function renderTagList(data) {
    let html = '<table><tr><th>ID</th><th>名称</th></tr>';
    data.forEach(t => {
        html += `<tr><td>${t.tag_id}</td><td>${t.name}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('tag-list').innerHTML = html;
}
document.getElementById('search-tag').addEventListener('input', function() {
    const val = this.value.trim();
    if (!val) return renderTagList(allTags);
    const filtered = allTags.filter(t => t.name && t.name.includes(val));
    renderTagList(filtered);
});
loadTags();

// 添加标签（不传ID，只传name）
document.getElementById('addTagForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const data = {
        name: document.getElementById('tag_name').value
    };
    fetch('http://localhost:5000/api/tags', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadTags();
        document.getElementById('addTagForm').reset();
    });
});

// 删除标签
document.getElementById('deleteTagForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const tag_id = document.getElementById('delete_tag_id').value;
    fetch(`http://localhost:5000/api/tags/${tag_id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadTags();
        document.getElementById('deleteTagForm').reset();
    });
});

// 角色-标签关联列表和搜索
let allCharacterTags = [];
function loadCharacterTags() {
    fetch('http://localhost:5000/api/character_tags')
        .then(res => res.json())
        .then(data => {
            allCharacterTags = data;
            renderCharacterTagList(data);
        });
}
function renderCharacterTagList(data) {
    let html = '<table><tr><th>角色ID</th><th>标签ID</th></tr>';
    data.forEach(ct => {
        html += `<tr><td>${ct.character_id}</td><td>${ct.tag_id}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('character-tag-list').innerHTML = html;
}
document.getElementById('search-character-tag').addEventListener('input', function() {
    const val = this.value.trim();
    if (!val) return renderCharacterTagList(allCharacterTags);
    const filtered = allCharacterTags.filter(ct =>
        (ct.character_id + '').includes(val) || (ct.tag_id + '').includes(val)
    );
    renderCharacterTagList(filtered);
});
loadCharacterTags();

// 添加角色-标签关联
document.getElementById('addCharacterTagForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const data = {
        character_id: document.getElementById('ct_character_id').value,
        tag_id: document.getElementById('ct_tag_id').value
    };
    fetch('http://localhost:5000/api/character_tags', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadCharacterTags();
        document.getElementById('addCharacterTagForm').reset();
    });
});

// 删除角色-标签关联
document.getElementById('deleteCharacterTagForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const character_id = document.getElementById('del_ct_character_id').value;
    const tag_id = document.getElementById('del_ct_tag_id').value;
    fetch(`http://localhost:5000/api/character_tags/${character_id}/${tag_id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadCharacterTags();
        document.getElementById('deleteCharacterTagForm').reset();
    });
});

// BOSS-标签关联列表和搜索
let allBossTags = [];
function loadBossTags() {
    fetch('http://localhost:5000/api/boss_tags')
        .then(res => res.json())
        .then(data => {
            allBossTags = data;
            renderBossTagList(data);
        });
}
function renderBossTagList(data) {
    let html = '<table><tr><th>BOSS ID</th><th>标签ID</th></tr>';
    data.forEach(bt => {
        html += `<tr><td>${bt.boss_id}</td><td>${bt.tag_id}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('boss-tag-list').innerHTML = html;
}
document.getElementById('search-boss-tag').addEventListener('input', function() {
    const val = this.value.trim();
    if (!val) return renderBossTagList(allBossTags);
    const filtered = allBossTags.filter(bt =>
        (bt.boss_id + '').includes(val) || (bt.tag_id + '').includes(val)
    );
    renderBossTagList(filtered);
});
loadBossTags();

// 添加BOSS-标签关联
document.getElementById('addBossTagForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const data = {
        boss_id: document.getElementById('bt_boss_id').value,
        tag_id: document.getElementById('bt_tag_id').value
    };
    fetch('http://localhost:5000/api/boss_tags', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadBossTags();
        document.getElementById('addBossTagForm').reset();
    });
});

// 删除BOSS-标签关联
document.getElementById('deleteBossTagForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const boss_id = document.getElementById('del_bt_boss_id').value;
    const tag_id = document.getElementById('del_bt_tag_id').value;
    fetch(`http://localhost:5000/api/boss_tags/${boss_id}/${tag_id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadBossTags();
        document.getElementById('deleteBossTagForm').reset();
    });
});

// 环境-标签关联列表和搜索
let allEnvTags = [];
function loadEnvTags() {
    fetch('http://localhost:5000/api/environment_tags')
        .then(res => res.json())
        .then(data => {
            allEnvTags = data;
            renderEnvTagList(data);
        });
}
function renderEnvTagList(data) {
    let html = '<table><tr><th>环境ID</th><th>标签ID</th></tr>';
    data.forEach(et => {
        html += `<tr><td>${et.env_id}</td><td>${et.tag_id}</td></tr>`;
    });
    html += '</table>';
    document.getElementById('env-tag-list').innerHTML = html;
}
document.getElementById('search-env-tag').addEventListener('input', function() {
    const val = this.value.trim();
    if (!val) return renderEnvTagList(allEnvTags);
    const filtered = allEnvTags.filter(et =>
        (et.env_id + '').includes(val) || (et.tag_id + '').includes(val)
    );
    renderEnvTagList(filtered);
});
loadEnvTags();

// 添加环境-标签关联
document.getElementById('addEnvTagForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const data = {
        env_id: document.getElementById('et_env_id').value,
        tag_id: document.getElementById('et_tag_id').value
    };
    fetch('http://localhost:5000/api/environment_tags', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadEnvTags();
        document.getElementById('addEnvTagForm').reset();
    });
});

// 删除环境-标签关联
document.getElementById('deleteEnvTagForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const env_id = document.getElementById('del_et_env_id').value;
    const tag_id = document.getElementById('del_et_tag_id').value;
    fetch(`http://localhost:5000/api/environment_tags/${env_id}/${tag_id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(res => {
        alert(res.message || res.error);
        loadEnvTags();
        document.getElementById('deleteEnvTagForm').reset();
    });
}); 