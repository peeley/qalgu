const submitToAPI= async () =>{
    let form = document.getElementById("input").elements['inputText'];
    let result = document.getElementById("output");
    let formText = form.value;
    fetch("./translate?q=" + formText)
        .then( (res)=>{
            res.json().then( (data) =>{
                result.innerHTML = data;
                form.value = "";
            });
        })   
        .catch((err) => {
            console.log(err);
            return;
        });
}
// TODO: refactor to React
let root = document.getElementById("root");
ReactDOM.render(<>, root);
