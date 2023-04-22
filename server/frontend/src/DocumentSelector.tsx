import * as React from 'react'
export default () => {
    const [docList, setDocList] = React.useState<string[]>(JSON.parse(localStorage.getItem("__docList") || "[]"))
    React.useEffect(() => {
        localStorage.setItem("__docList", JSON.stringify(docList))
    }, [docList])
    const [newDocName, setNewDocName] = React.useState<string>("");
    return (<div>
        <h1>Pick a document</h1>
        <div style={{ display: 'flex', flexDirection: "column" }}>
            {docList.map((doc, idx) => (
                <a key={idx} href={`/docs/${doc}`} >{doc}</a>
            ))}
        </div>
        <input onChange={evt => setNewDocName(evt.target.value)} value={newDocName} placeholder="new document"></input>
        <button onClick={() => setDocList([...docList, newDocName])}>Make new document</button>
    </div >)
}