from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)
DB = "wmp.db"

# ---------- DATABASE ----------
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.execute("""
    CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        height TEXT,
        eye_color TEXT,
        case_name TEXT,
        crimes TEXT,
        warrant INTEGER,
        surveillance INTEGER,
        safe INTEGER,
        in_custody INTEGER,
        notes TEXT
    )
    """)
    db.commit()
    db.close()

# ---------- API ----------
@app.route("/api/persons", methods=["GET"])
def get_persons():
    db = get_db()
    data = db.execute("SELECT * FROM persons").fetchall()
    db.close()
    return jsonify([dict(p) for p in data])

@app.route("/api/persons", methods=["POST"])
def add_person():
    d = request.json
    db = get_db()
    db.execute("""
        INSERT INTO persons
        (name, age, height, eye_color, case_name, crimes, warrant, surveillance, safe, in_custody, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        d["name"], d["age"], d["height"], d["eye_color"], d["case_name"],
        d["crimes"], d["warrant"], d["surveillance"], d["safe"],
        d["in_custody"], d["notes"]
    ))
    db.commit()
    db.close()
    return jsonify({"status": "saved"})

@app.route("/api/persons/<int:pid>", methods=["PUT"])
def update_person(pid):
    d = request.json
    db = get_db()
    db.execute("""
        UPDATE persons SET
        name=?, age=?, height=?, eye_color=?, case_name=?, crimes=?,
        warrant=?, surveillance=?, safe=?, in_custody=?, notes=?
        WHERE id=?
    """, (
        d["name"], d["age"], d["height"], d["eye_color"], d["case_name"],
        d["crimes"], d["warrant"], d["surveillance"], d["safe"],
        d["in_custody"], d["notes"], pid
    ))
    db.commit()
    db.close()
    return jsonify({"status": "updated"})

@app.route("/api/persons/<int:pid>", methods=["DELETE"])
def delete_person(pid):
    code = request.args.get("code")
    if code != "2025":
        return jsonify({"error": "Invalid delete code"}), 403
    db = get_db()
    db.execute("DELETE FROM persons WHERE id=?", (pid,))
    db.commit()
    db.close()
    return jsonify({"status": "deleted"})

# ---------- UI ----------
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>WMP Person System</title>
<style>
body { margin:0; font-family:Arial; background:#f5f5f5; }
.app { display:flex; padding:20px; }
.sidebar { width:220px; }
.btn {
    width:100%; padding:15px; margin-bottom:15px;
    background:#b0b0b0; border:1px solid #666;
    font-weight:bold; cursor:pointer; font-size:16px;
}
.main { flex:1; margin-left:30px; display:flex; gap:30px; }
.list { width:45%; display:flex; flex-direction:column; gap:20px; }
.card {
    background:#a6a6a6; padding:22px; border-radius:8px;
    display:flex; justify-content:space-between;
    font-weight:bold; font-size:17px; cursor:pointer;
}
.detail {
    width:55%; background:#d0d0d0; padding:25px;
    border-radius:10px; display:none;
}
.detail h2 { margin-top:0; }
.field { margin-bottom:12px; }
.field label { font-weight:bold; display:block; }
.field input, .field textarea {
    width:100%; padding:8px; font-size:15px;
}
.checkbox { display:flex; gap:10px; margin-bottom:8px; }
.save { background:#4caf50; color:#fff; }
.delete { background:#c62828; color:#fff; }
</style>
</head>
<body>

<div class="app">
<div class="sidebar">
    <button class="btn" onclick="newPerson()">NEW PERSON</button>
</div>

<div class="main">
    <div class="list" id="list"></div>

    <div class="detail" id="detail">
        <h2>Person Details</h2>

        <div id="form"></div>

        <button class="btn save" onclick="save()">SAVE</button>
        <button class="btn delete" onclick="remove()">DELETE</button>
    </div>
</div>
</div>

<script>
let persons=[], current=null;

function load(){
 fetch("/api/persons").then(r=>r.json()).then(d=>{persons=d; render();});
}

function render(){
 const l=document.getElementById("list"); l.innerHTML="";
 persons.forEach(p=>{
  const c=document.createElement("div");
  c.className="card";
  c.innerHTML=`<span>${p.name}</span><span>${p.case_name}</span>`;
  c.onclick=()=>open(p);
  l.appendChild(c);
 });
}

function open(p){
 current=p;
 document.getElementById("detail").style.display="block";
 document.getElementById("form").innerHTML=`
  ${input("Name","name")}
  ${input("Age","age")}
  ${input("Height","height")}
  ${input("Eye Color","eye_color")}
  ${input("Case","case_name")}
  ${input("Crimes","crimes")}
  ${check("Arrest Warrant","warrant")}
  ${check("Under Surveillance","surveillance")}
  ${check("Clean / Safe","safe")}
  ${check("In Custody","in_custody")}
  ${textarea("Notes","notes")}
 `;
}

function input(label,key){
 return `<div class="field"><label>${label}</label>
 <input id="${key}" value="${current[key]||""}"></div>`;
}
function textarea(label,key){
 return `<div class="field"><label>${label}</label>
 <textarea id="${key}">${current[key]||""}</textarea></div>`;
}
function check(label,key){
 return `<div class="checkbox">
 <input type="checkbox" id="${key}" ${current[key]?"checked":""}>
 <label>${label}</label></div>`;
}

function save(){
 fetch("/api/persons/"+current.id,{
  method:"PUT",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify(collect())
 }).then(load);
}

function remove(){
 const code=prompt("Enter DELETE code");
 if(code!=="2025") return alert("Wrong code");
 fetch("/api/persons/"+current.id+"?code=2025",{method:"DELETE"}).then(()=>{
  document.getElementById("detail").style.display="none";
  load();
 });
}

function collect(){
 return {
  name:v("name"), age:v("age"), height:v("height"), eye_color:v("eye_color"),
  case_name:v("case_name"), crimes:v("crimes"),
  warrant:c("warrant"), surveillance:c("surveillance"),
  safe:c("safe"), in_custody:c("in_custody"), notes:v("notes")
 };
}
function v(id){return document.getElementById(id).value;}
function c(id){return document.getElementById(id).checked?1:0;}

function newPerson(){
 fetch("/api/persons",{method:"POST",headers:{"Content-Type":"application/json"},
 body:JSON.stringify({
  name:"New Person",age:0,height:"",eye_color:"",
  case_name:"",crimes:"",warrant:0,surveillance:0,
  safe:1,in_custody:0,notes:""
 })}).then(load);
}

load();
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
