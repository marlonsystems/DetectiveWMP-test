async function loadPersons() {
    const res = await fetch("/persons");
    const data = await res.json();

    const list = document.getElementById("personList");
    list.innerHTML = "";

    data.forEach(p => {
        const li = document.createElement("li");
        li.textContent = `${p.first_name} ${p.last_name} (${p.role})`;
        list.appendChild(li);
    });
}

async function addPerson() {
    await fetch("/persons", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            first_name: document.getElementById("firstName").value,
            last_name: document.getElementById("lastName").value,
            role: document.getElementById("role").value
        })
    });

    loadPersons();
}

async function loadCases() {
    const res = await fetch("/cases");
    const data = await res.json();

    const list = document.getElementById("caseList");
    list.innerHTML = "";

    data.forEach(c => {
        const li = document.createElement("li");
        li.textContent = `${c.title} [${c.priority}]`;
        list.appendChild(li);
    });
}

async function addCase() {
    await fetch("/cases", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            title: document.getElementById("caseTitle").value,
            priority: document.getElementById("casePriority").value
        })
    });

    loadCases();
}

loadPersons();
loadCases();
