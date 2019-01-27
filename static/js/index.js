let root = document.getElementById("root");
let cookie = document.cookie;
let username = "randoName";
let weekFromNow = new Date(Date.now() + 60*60);
cookie += `name=${username}; expires=${weekFromNow.toGMTString()}; path=/;`;
console.log(`${cookie}`);
const URL = '/translate?q=';
class Translator extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            inputText : undefined,
            output : "Translated Inupiaq text will appear here!",
        };
    }
    render(){
        return(
			<form id='input' onSubmit={this.submitToAPI}>
				<div className="container">
				<div className="row">
					<div className="col">
						<label>English:</label>
						<textarea id='inputText' rows="5" wrap='hard' className='form-control'
							value={this.state.inputText} onChange={this.handleChange}
							placeholder={this.state.inputText === undefined ? "Enter English text here!" : ""}>
						</textarea>
					</div>
					<div className="col">
						<p> Inupiaq: </p>
						<p>{this.state.output}</p>
                        <button className="btn btn-info" onClick={this.rememberTranslation}>Save Translation</button>
					</div>
				</div>
				</div>
			</form>
        );
    }
    handleChange = (event) => {
        let eventValue = event.target.value;
        this.setState({ inputText : eventValue }, () => {
            if(eventValue != ""){
                this.submitToAPI(eventValue);
            }
            else{
                this.setState({ output : "" });
            }
        });
        event.preventDefault();
    }
    submitToAPI = async (eventValue) => {
		let url = URL + eventValue;
        fetch(url)
		  .then(response => response.json())
		  .then(json => {
			this.setState({output : json });
		  })
		  .catch(err => {
			  alert("Error: " + err);
			  console.log(err)
		  });
    }
    rememberTranslation = (event) => {
        cookie += `${this.state.inputText} : ${this.state.output}`;
        console.log(cookie);
        event.preventDefault();
    }
}
ReactDOM.render(<Translator />, root);
