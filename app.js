document.addEventListener('DOMContentLoaded', () => {
    fetch('vocabulary.md')
        .then(response => response.text())
        .then(content => {
            const data = parseMdContent(content);
            populateTable(data);
        })
        .catch(error => console.error('Error fetching the vocabulary file:', error));
});

function parseMdContent(content) {
    const pattern = /### (.*?)（.*?）\n\n\*\*全称\*\*：(.*?)\n\n\*\*中文\*\*：(.*?)\n\n\*\*介绍\*\*：(.*?)\n/g;
    const matches = [];
    let match;
    while ((match = pattern.exec(content)) !== null) {
        matches.push({
            缩写: match[1],
            全称: match[2],
            中文: match[3],
            介绍: match[4].trim()
        });
    }
    return matches;
}

function populateTable(data) {
    const tbody = document.querySelector('#vocabularyTable tbody');
    tbody.innerHTML = '';
    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.缩写}</td>
            <td>${item.全称}</td>
            <td>${item.中文}</td>
            <td>${item.介绍}</td>
        `;
        tbody.appendChild(row);
    });
}

function toggleColumn(column) {
    const index = {
        '缩写': 0,
        '全称': 1,
        '中文': 2,
        '介绍': 3
    }[column];
    const cells = document.querySelectorAll(`#vocabularyTable td:nth-child(${index + 1}), #vocabularyTable th:nth-child(${index + 1})`);
    cells.forEach(cell => {
        cell.classList.toggle('hidden');
    });
}
